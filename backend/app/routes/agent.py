"""
Agent-related routes for managing AI agents and their content.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Form
from typing import Dict, Any, Optional
from datetime import datetime
from app.services.telegram_service import TelegramService
from app.services.db_service import create_agent, get_agent_by_id, list_agents, delete_agent, save_chat_message
from app.services.openai_service import generate_embedding
from app.services.pinecone_service import upsert_vectors
from app.utils.logger import logger
from uuid import uuid4
from app.services.rag_service import rag_retrieve_and_summarize

router = APIRouter()

@router.get("/list")
async def list_agents_route():
    """
    List all available agents.
    """
    try:
        agents = await list_agents()
        return {
            "agents": agents,
            "status": "success"
        }
    except Exception as e:
        logger.error("Failed to list agents: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}")
async def get_agent(agent_id: str) -> Dict[str, Any]:
    """
    Retrieve agent information by ID.
    """
    agent = await get_agent_by_id(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.post("/create")
async def create_agent_from_channel(
    channel_link: str = Form(...),
    prompt_template: str = Form(...),
    owner_id: str = Form(...),
    limit: Optional[int] = Form(None),
    min_id: Optional[int] = Form(None),
    offset_date: Optional[datetime] = Form(None)
) -> Dict[str, Any]:
    """
    Create a new agent from a Telegram channel and start ingesting its content.
    
    Args:
        channel_link: The Telegram channel link or username
        prompt_template: Template for agent's responses
        owner_id: ID of the user creating this agent
        limit: Optional limit on number of messages to ingest
        min_id: Optional minimum message ID to start from
        offset_date: Optional date to start ingestion from
    """
    try:
        # Initialize Telegram service
        async with TelegramService() as telegram:
            # Get channel info first
            channel_info = await telegram.get_channel_info(channel_link)
            channel_title = channel_info["title"]
            
            # Create agent in database using channel title as expert name
            logger.info("Creating agent for channel: %s with title: %s", channel_link, channel_title)
            agent = await create_agent(owner_id, channel_title, prompt_template)
            agent_id = agent["id"]
            
            # Fetch messages from channel
            messages = await telegram.get_channel_messages(
                channel_link=channel_link,
                limit=limit,
                min_id=min_id,
                offset_date=offset_date
            )
            
            if not messages:
                logger.warning("No messages found in channel: %s", channel_link)
                return {
                    "agent_id": agent_id,
                    "message_count": 0,
                    "status": "created_without_messages"
                }
            
            # Process messages in batches
            batch_size = 100
            total_vectors = 0
            
            for i in range(0, len(messages), batch_size):
                batch = messages[i:i + batch_size]
                
                # Generate embeddings for batch
                vectors = []
                metadata = []
                ids = []
                
                for msg in batch:
                    # Skip empty messages
                    if not msg["text"].strip():
                        continue
                    
                    # Generate embedding
                    embedding = await generate_embedding(msg["text"])
                    if not embedding:
                        continue
                    
                    vectors.append(embedding)
                    metadata.append({
                        "agent_id": agent_id,
                        "source_link": msg["link"],
                        "text": msg["text"],
                        "date": msg["date"],
                        "views": msg["views"],
                        "forwards": msg["forwards"]
                    })
                    ids.append(str(uuid4()))
                
                if vectors:
                    # Upsert vectors to Pinecone
                    success = await upsert_vectors(vectors, metadata, ids)
                    if success:
                        total_vectors += len(vectors)
                        logger.info(
                            "Processed batch of %d messages for channel %s (total vectors: %d)",
                            len(vectors), channel_link, total_vectors
                        )
            
            return {
                "agent_id": agent_id,
                "message_count": len(messages),
                "vector_count": total_vectors,
                "status": "success"
            }
            
    except Exception as e:
        logger.error("Failed to create agent from channel %s: %s", channel_link, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{agent_id}")
async def delete_agent_route(agent_id: str) -> Dict[str, Any]:
    """
    Delete an agent by ID.
    """
    try:
        success = await delete_agent(agent_id)
        if not success:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {
            "status": "success",
            "message": f"Agent {agent_id} deleted successfully"
        }
    except Exception as e:
        logger.error("Failed to delete agent: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{agent_id}/chat")
async def chat_with_agent(
    agent_id: str,
    message: str = Form(...),
    user_id: str = Form(...)
) -> Dict[str, Any]:
    """
    Chat with an agent using RAG.
    
    Args:
        agent_id: The ID of the agent to chat with
        message: The user's message
        user_id: The ID of the user sending the message
        
    Returns:
        The agent's response
    """
    try:
        # Get agent details
        agent = await get_agent_by_id(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
            
        try:
            # Save user message
            await save_chat_message(
                agent_id=agent_id,
                user_id=user_id,
                role="user",
                content=message
            )
        except Exception as e:
            logger.error("Failed to save user message: %s", str(e))
            raise HTTPException(
                status_code=400,
                detail=f"Failed to save message: {str(e)}"
            )
        
        try:
            # Get response using RAG
            response = await rag_retrieve_and_summarize(
                query=message,
                agent_id=agent_id,
                mode="chat"
            )
        except Exception as e:
            logger.error("Failed to generate response: %s", str(e))
            raise HTTPException(
                status_code=500,
                detail="Failed to generate response"
            )
        
        try:
            # Save agent response
            await save_chat_message(
                agent_id=agent_id,
                user_id=user_id,
                role="agent",
                content=response
            )
        except Exception as e:
            logger.error("Failed to save agent response: %s", str(e))
            # Don't fail the request if saving the response fails
            # The user still gets their answer
            
        return {
            "response": response,
            "status": "success"
        }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to process chat message: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        ) 