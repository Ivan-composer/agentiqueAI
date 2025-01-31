"""
Chat-related routes for interacting with AI agents.
"""
from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID
from app.models.db_models import ChatMessage, ChatMessageCreate
from app.services.db_service import save_chat_message

router = APIRouter()

@router.post("/", response_model=ChatMessage)
async def send_message(message: ChatMessageCreate):
    """Send a message to an agent."""
    try:
        saved_message = await save_chat_message(
            agent_id=str(message.agent_id),
            user_id=str(message.user_id),
            role=message.role,
            content=message.content
        )
        return saved_message
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 