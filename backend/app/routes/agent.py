"""
Agent-related routes for managing AI agents and their content.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Form, File, UploadFile
from typing import Dict, Any, Optional
from datetime import datetime
from app.services.telegram_service import TelegramService
from app.services.db_service import create_agent, get_agent_by_id, list_agents, delete_agent, save_chat_message, get_chat_history
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
    profile_photo: Optional[UploadFile] = File(None),
    channel_title: Optional[str] = Form(None),
    channel_username: Optional[str] = Form(None),
    channel_description: Optional[str] = Form(None),
    channel_participants: Optional[int] = Form(None),
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
        profile_photo: Optional profile photo file
        channel_title: Optional channel title
        channel_username: Optional channel username
        channel_description: Optional channel description
        channel_participants: Optional number of channel participants
        limit: Optional limit on number of messages to ingest
        min_id: Optional minimum message ID to start from
        offset_date: Optional date to start ingestion from
    """
    try:
        # Initialize Telegram service
        async with TelegramService() as telegram:
            # Get channel info first
            logger.info("Fetching channel info for: %s", channel_link)
            
            # Prepare channel info
            channel_info = {
                "title": channel_title,
                "username": channel_username,
                "description": channel_description,
                "participants_count": channel_participants
            }
            
            # Handle profile photo if provided
            if profile_photo:
                photo_data = await profile_photo.read()
                channel_info["profile_photo"] = photo_data
                logger.info("Profile photo received, size: %d bytes", len(photo_data))
            
            # Create agent in database with channel info
            logger.info("Creating agent for channel: %s with title: %s", channel_link, channel_info["title"])
            agent = await create_agent(
                owner_id=owner_id,
                expert_name=channel_info["title"] or "Unnamed Agent",
                prompt_template=prompt_template,
                channel_info=channel_info
            )
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
                    "status": "created_without_messages",
                    "agent": agent  # Include full agent info in response
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
                "status": "success",
                "agent": agent  # Include full agent info in response
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
        logger.info("Chat request - agent_id: %s, user_id: %s", agent_id, user_id)
        logger.debug("Message content: %s", message)
        
        # Get agent details
        agent = await get_agent_by_id(agent_id)
        if not agent:
            logger.error("Agent not found: %s", agent_id)
            raise HTTPException(status_code=404, detail="Agent not found")
        logger.debug("Found agent: %s", agent)
            
        try:
            # Save user message
            logger.info("Saving user message...")
            user_message = await save_chat_message(
                agent_id=agent_id,
                user_id=user_id,
                role="user",
                content=message
            )
            logger.debug("Saved user message: %s", user_message)
        except Exception as e:
            logger.error("Failed to save user message: %s", str(e), exc_info=True)
            raise HTTPException(
                status_code=400,
                detail=f"Failed to save message: {str(e)}"
            )
        
        try:
            # Get response using RAG
            logger.info("Generating agent response...")
            response = await rag_retrieve_and_summarize(
                query=message,
                agent_id=agent_id,
                mode="chat"
            )
            logger.debug("Generated response: %s", response)
        except Exception as e:
            logger.error("Failed to generate response: %s", str(e), exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Failed to generate response"
            )
        
        try:
            # Save agent response
            logger.info("Saving agent response...")
            agent_message = await save_chat_message(
                agent_id=agent_id,
                user_id=user_id,
                role="agent",
                content=response
            )
            logger.debug("Saved agent message: %s", agent_message)
        except Exception as e:
            logger.error("Failed to save agent response: %s", str(e), exc_info=True)
            # Don't fail the request if saving the response fails
            # The user still gets their answer
            
        return {
            "response": response,
            "status": "success",
            "user_message": user_message,
            "agent_message": agent_message
        }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to process chat message: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )

@router.get("/{agent_id}/chat_history")
async def get_agent_chat_history(
    agent_id: str,
    user_id: str,
    limit: int = 50,
    before_timestamp: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Get chat history between a user and an agent.
    
    Args:
        agent_id: The ID of the agent
        user_id: The ID of the user
        limit: Maximum number of messages to return
        before_timestamp: Only return messages before this timestamp
        
    Returns:
        Dictionary containing chat messages and metadata
    """
    try:
        logger.info(
            "Chat history request - agent_id: %s, user_id: %s, limit: %d", 
            agent_id, user_id, limit
        )
        if before_timestamp:
            logger.debug("Before timestamp: %s", before_timestamp)
            
        # Get agent details
        agent = await get_agent_by_id(agent_id)
        if not agent:
            logger.error("Agent not found: %s", agent_id)
            raise HTTPException(status_code=404, detail="Agent not found")
        logger.debug("Found agent: %s", agent)
            
        try:
            # Get chat history
            logger.info("Retrieving chat history...")
            messages = await get_chat_history(
                agent_id=agent_id,
                user_id=user_id,
                limit=limit,
                before_timestamp=before_timestamp
            )
            logger.debug("Retrieved %d messages", len(messages))
            
            return {
                "messages": messages,
                "status": "success",
                "agent": agent
            }
            
        except Exception as e:
            logger.error(
                "Failed to retrieve chat history: %s", 
                str(e), 
                exc_info=True
            )
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve chat history"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to process chat history request: %s",
            str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        ) 