import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing required Supabase environment variables")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_user_by_telegram_id(telegram_id: str):
    """Get user by Telegram ID"""
    response = supabase.table("users").select("*").eq("telegram_id", telegram_id).execute()
    return response.data[0] if response.data else None

async def create_user(telegram_id: str, username: str = None):
    """Create a new user"""
    user_data = {
        "telegram_id": telegram_id,
        "username": username,
        "credits_balance": 10  # Default starting credits
    }
    response = supabase.table("users").insert(user_data).execute()
    return response.data[0] if response.data else None

async def get_user_agents(user_id: str):
    """Get all agents for a user"""
    response = supabase.table("agents").select("*").eq("user_id", user_id).execute()
    return response.data

async def get_agent(agent_id: str):
    """Get agent by ID"""
    response = supabase.table("agents").select("*").eq("id", agent_id).execute()
    return response.data[0] if response.data else None

async def create_agent(user_id: str, name: str, channel_link: str):
    """Create a new agent"""
    agent_data = {
        "user_id": user_id,
        "name": name,
        "channel_link": channel_link,
        "status": "ingesting"  # Initial status while ingesting data
    }
    response = supabase.table("agents").insert(agent_data).execute()
    return response.data[0] if response.data else None
            
async def update_agent_status(agent_id: str, status: str):
    """Update agent status"""
    response = supabase.table("agents").update({"status": status}).eq("id", agent_id).execute()
    return response.data[0] if response.data else None

async def record_chat(
    user_id: str,
    agent_id: str,
    message: str,
    response: str,
    context: str = "",
    sources: List[Dict[str, Any]] = None
) -> bool:
    """Record a chat interaction in the database"""
    try:
        chat_data = {
            "user_id": user_id,
            "agent_id": agent_id,
            "message": message,
            "response": response,
            "context": context,
            "sources": sources or [],
            "created_at": "now()"
        }
        
        result = supabase.table("chat_messages").insert(chat_data).execute()
        return bool(result.data)
        
    except Exception as e:
        print(f"Error recording chat: {str(e)}")
        return False

async def deduct_credits(user_id: str, amount: int, description: str) -> bool:
    """
    Deduct credits from user balance and record transaction
    Returns True if successful, False if insufficient credits
    """
    # Get current balance
    user = supabase.table("users").select("credits_balance").eq("id", user_id).execute()
    if not user.data:
        return False
    
    current_balance = user.data[0]["credits_balance"]
    if current_balance < amount:
        return False
    
    # Update balance
    supabase.table("users").update(
        {"credits_balance": current_balance - amount}
    ).eq("id", user_id).execute()
    
    # Record transaction
    transaction_data = {
        "user_id": user_id,
        "amount": amount,
        "type": "debit",
        "description": description
    }
    supabase.table("transactions").insert(transaction_data).execute()
    
    return True

async def add_credits(user_id: str, amount: int, description: str):
    """Add credits to user balance and record transaction"""
    # Get current balance
    user = supabase.table("users").select("credits_balance").eq("id", user_id).execute()
    if not user.data:
        return False
    
    current_balance = user.data[0]["credits_balance"]
    
    # Update balance
    supabase.table("users").update(
        {"credits_balance": current_balance + amount}
    ).eq("id", user_id).execute()
    
    # Record transaction
    transaction_data = {
        "user_id": user_id,
        "amount": amount,
        "type": "credit",
        "description": description
    }
    supabase.table("transactions").insert(transaction_data).execute()
    
    return True

async def get_chat_history(agent_id: str, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get chat history for a specific agent and user"""
    response = supabase.table("chat_messages") \
        .select("*") \
        .eq("agent_id", agent_id) \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .limit(limit) \
        .execute()
    return response.data if response.data else []

async def clear_chat_history(agent_id: str, user_id: str) -> bool:
    """Clear chat history for a specific agent and user"""
    try:
        response = supabase.table("chat_messages") \
            .delete() \
            .eq("agent_id", agent_id) \
            .eq("user_id", user_id) \
            .execute()
        return True
    except Exception as e:
        print(f"Error clearing chat history: {str(e)}")
        return False 