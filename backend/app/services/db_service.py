"""
Database service for Supabase interactions.
Handles all database operations and provides a clean interface for data access.
"""
import os
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv
from app.utils.logger import logger
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    logger.error("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

logger.info("Initializing Supabase client with URL: %s", supabase_url)
supabase: Client = create_client(
    supabase_url=supabase_url,
    supabase_key=supabase_key
)

async def get_user_by_telegram_id(telegram_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user by their Telegram ID.
    """
    logger.debug("Fetching user with telegram_id: %s", telegram_id)
    response = supabase.table("users").select("*").eq("telegram_id", telegram_id).execute()
    if response.data:
        logger.info("Found user with telegram_id: %s", telegram_id)
        return response.data[0]
    logger.info("No user found with telegram_id: %s", telegram_id)
    return None

async def create_user(telegram_id: str, username: str) -> Dict[str, Any]:
    """
    Create a new user with the given Telegram ID and username.
    """
    logger.info("Creating new user with telegram_id: %s, username: %s", telegram_id, username)
    user_data = {
        "telegram_id": telegram_id,
        "username": username,
        "credits_balance": 0  # Default starting balance
    }
    try:
        response = supabase.table("users").insert(user_data).execute()
        logger.info("Successfully created user with telegram_id: %s", telegram_id)
        return response.data[0]
    except Exception as e:
        logger.error("Failed to create user with telegram_id: %s - %s", telegram_id, str(e))
        raise

async def get_agent_by_id(agent_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve an agent by its ID.
    """
    logger.debug("Fetching agent with id: %s", agent_id)
    response = supabase.table("agents").select("*").eq("id", agent_id).execute()
    if response.data:
        logger.info("Found agent with id: %s", agent_id)
        return response.data[0]
    logger.info("No agent found with id: %s", agent_id)
    return None

async def create_agent(
    owner_id: str,
    expert_name: str,
    prompt_template: str,
    channel_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a new agent for a user.
    
    Args:
        owner_id: The ID of the agent owner
        expert_name: The name of the expert/agent
        prompt_template: The prompt template for the agent
        channel_info: Dictionary containing channel information including profile picture
        
    Returns:
        The created agent record
        
    Raises:
        Exception: If agent creation fails
    """
    logger.info("Creating new agent for owner_id: %s, expert_name: %s", owner_id, expert_name)
    logger.debug("Channel info received: %s", channel_info)
    
    # Upload profile photo to Supabase storage if available
    profile_photo_url = None
    if channel_info.get("profile_photo"):
        try:
            logger.info("Profile photo data received, size: %d bytes", len(channel_info["profile_photo"]))
            
            # Generate unique filename
            photo_filename = f"agent_photos/{owner_id}_{int(datetime.now().timestamp())}.jpg"
            logger.info("Generated filename: %s", photo_filename)
            
            # Upload to Supabase storage
            logger.info("Uploading to Supabase storage...")
            response = supabase.storage.from_("agent-photos").upload(
                path=photo_filename,
                file=channel_info["profile_photo"],
                file_options={"content-type": "image/jpeg"}
            )
            logger.info("Upload response: %s", response)
            
            # Get public URL
            profile_photo_url = supabase.storage.from_("agent-photos").get_public_url(photo_filename)
            logger.info("Successfully uploaded profile photo: %s", profile_photo_url)
            
        except Exception as e:
            logger.error("Failed to upload profile photo: %s", str(e), exc_info=True)
            logger.error("Error type: %s", type(e).__name__)
    else:
        logger.warning("No profile photo found in channel info")
    
    agent_data = {
        "owner_id": owner_id,
        "expert_name": expert_name,
        "prompt_template": prompt_template,
        "status": "active",
        "profile_photo_url": profile_photo_url,
        "channel_title": channel_info.get("title"),
        "channel_username": channel_info.get("username"),
        "channel_description": channel_info.get("description"),
        "channel_participants": channel_info.get("participants_count", 0)
    }
    
    try:
        response = supabase.table("agents").insert(agent_data).execute()
        logger.info("Successfully created agent with id: %s", response.data[0]["id"])
        return response.data[0]
    except Exception as e:
        logger.error("Failed to create agent for owner_id: %s - %s", owner_id, str(e))
        raise

async def save_chat_message(
    agent_id: str,
    user_id: str,
    role: str,
    content: str
) -> Dict[str, Any]:
    """
    Save a chat message to the database.
    
    Args:
        agent_id: The ID of the agent
        user_id: The ID of the user
        role: The role of the message sender ('user' or 'agent')
        content: The message content
        
    Returns:
        The created message record
        
    Raises:
        Exception: If message creation fails
    """
    logger.info("Saving chat message - agent_id: %s, user_id: %s, role: %s", agent_id, user_id, role)
    logger.debug("Message content: %s", content)
    
    message_data = {
        "agent_id": agent_id,
        "user_id": user_id,
        "role": role,
        "content": content
        # created_at will be set automatically by the database
    }
    
    try:
        logger.debug("Inserting message into database: %s", message_data)
        response = supabase.table("chat_messages").insert(message_data).execute()
        logger.info("Successfully saved chat message with id: %s", response.data[0]["id"])
        logger.debug("Saved message data: %s", response.data[0])
        return response.data[0]
    except Exception as e:
        logger.error("Failed to save chat message - %s", str(e), exc_info=True)
        logger.error("Error type: %s", type(e).__name__)
        raise

async def get_chat_history(
    agent_id: str,
    user_id: str,
    limit: int = 50,
    before_timestamp: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get chat history between a user and an agent.
    
    Args:
        agent_id: The ID of the agent
        user_id: The ID of the user
        limit: Maximum number of messages to return
        before_timestamp: Only return messages before this timestamp
        
    Returns:
        List of message records in chronological order
        
    Raises:
        Exception: If fetching messages fails
    """
    logger.info("Fetching chat history - agent_id: %s, user_id: %s, limit: %d", agent_id, user_id, limit)
    if before_timestamp:
        logger.debug("Fetching messages before: %s", before_timestamp)
    
    try:
        # Build query
        query = supabase.table("chat_messages")\
            .select("*")\
            .eq("agent_id", agent_id)\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .limit(limit)
        
        if before_timestamp:
            query = query.lt("created_at", before_timestamp)
        
        logger.debug("Executing query...")
        response = query.execute()
        logger.debug("Raw response data: %s", response.data)
        
        # Return messages in chronological order (oldest first)
        messages = sorted(response.data, key=lambda x: x["created_at"])
        logger.info("Successfully fetched %d messages", len(messages))
        logger.debug("Returning messages: %s", messages)
        return messages
        
    except Exception as e:
        logger.error("Failed to fetch chat history - %s", str(e), exc_info=True)
        logger.error("Error type: %s", type(e).__name__)
        raise

async def record_transaction(user_id: str, credits_change: int, reason: str) -> Dict[str, Any]:
    """
    Record a credits transaction for a user.
    """
    logger.info("Recording transaction for user_id: %s, credits_change: %d", user_id, credits_change)
    transaction_data = {
        "user_id": user_id,
        "credits_change": credits_change,
        "reason": reason
    }
    try:
        response = supabase.table("transactions").insert(transaction_data).execute()
        logger.info("Successfully recorded transaction with id: %s", response.data[0]["id"])
        return response.data[0]
    except Exception as e:
        logger.error("Failed to record transaction for user_id: %s - %s", user_id, str(e))
        raise

async def list_agents() -> List[Dict[str, Any]]:
    """
    List all active agents.
    """
    logger.debug("Fetching all active agents")
    try:
        response = supabase.table("agents").select("*").eq("status", "active").execute()
        logger.info("Successfully fetched %d agents", len(response.data))
        return response.data
    except Exception as e:
        logger.error("Failed to fetch agents - %s", str(e))
        raise

async def delete_agent(agent_id: str) -> bool:
    """
    Delete an agent by ID.
    
    Args:
        agent_id: The ID of the agent to delete
        
    Returns:
        bool: True if successful, False if agent not found
    """
    logger.debug("Deleting agent with id: %s", agent_id)
    try:
        response = supabase.table("agents").delete().eq("id", agent_id).execute()
        if response.data:
            logger.info("Successfully deleted agent with id: %s", agent_id)
            return True
        logger.info("No agent found with id: %s", agent_id)
        return False
    except Exception as e:
        logger.error("Failed to delete agent with id: %s - %s", agent_id, str(e))
        raise 