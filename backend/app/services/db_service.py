"""
Database service for Supabase interactions.
Handles all database operations and provides a clean interface for data access.
"""
import os
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv
from app.utils.logger import logger

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

async def create_agent(owner_id: str, expert_name: str, prompt_template: str) -> Dict[str, Any]:
    """
    Create a new agent for a user.
    """
    logger.info("Creating new agent for owner_id: %s, expert_name: %s", owner_id, expert_name)
    agent_data = {
        "owner_id": owner_id,
        "expert_name": expert_name,
        "prompt_template": prompt_template,
        "status": "active"
    }
    try:
        response = supabase.table("agents").insert(agent_data).execute()
        logger.info("Successfully created agent with id: %s", response.data[0]["id"])
        return response.data[0]
    except Exception as e:
        logger.error("Failed to create agent for owner_id: %s - %s", owner_id, str(e))
        raise

async def save_chat_message(agent_id: str, user_id: str, role: str, content: str) -> Dict[str, Any]:
    """
    Save a chat message to the database.
    """
    logger.debug("Saving chat message for agent_id: %s, user_id: %s", agent_id, user_id)
    message_data = {
        "agent_id": agent_id,
        "user_id": user_id,
        "role": role,
        "content": content
    }
    try:
        response = supabase.table("chat_messages").insert(message_data).execute()
        logger.info("Successfully saved chat message with id: %s", response.data[0]["id"])
        return response.data[0]
    except Exception as e:
        logger.error("Failed to save chat message - %s", str(e))
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