from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import logging

from ..services.db_service import (
    get_user_by_telegram_id,
    create_user,
    get_chat_history,
    clear_chat_history
)
from ..services.chat_service import get_agent_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class ChatMessage(BaseModel):
    agent_id: str
    message: str
    chat_history: Optional[List[Dict[str, str]]] = None

async def get_current_user() -> str:
    """Get current user ID for testing"""
    # For testing, get the test user
    test_user = await get_user_by_telegram_id("test_user")
    if not test_user:
        test_user = await create_user(
            telegram_id="test_user",
            username="test_user"
        )
    return test_user["id"]  # Return the UUID of the test user

@router.post("/chat/")
async def chat(
    message: ChatMessage,
    user_id: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Send a message to an agent and get a response
    """
    try:
        response = await get_agent_response(
            agent_id=message.agent_id,
            user_id=user_id,
            message=message.message,
            chat_history=message.chat_history
        )
        
        if not response:
            raise HTTPException(status_code=500, detail="Failed to get agent response")
            
        return {
            "success": True,
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history/{agent_id}")
async def get_history(
    agent_id: str,
    user_id: str = Depends(get_current_user),
    limit: int = 50
) -> Dict[str, Any]:
    """
    Get chat history for an agent
    """
    try:
        history = await get_chat_history(agent_id, user_id, limit)
        return {
            "success": True,
            "history": history
        }
        
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/chat/history/{agent_id}")
async def clear_history(
    agent_id: str,
    user_id: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Clear chat history for an agent
    """
    try:
        await clear_chat_history(agent_id, user_id)
        return {
            "success": True,
            "message": "Chat history cleared"
        }
        
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 