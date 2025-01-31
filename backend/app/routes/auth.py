"""
Authentication and user management routes.
"""
from fastapi import APIRouter, HTTPException
from app.models.db_models import User, UserCreate
from app.services.db_service import create_user, get_user_by_telegram_id

router = APIRouter()

@router.post("/telegram/login", response_model=User)
async def telegram_login(telegram_id: str, username: str):
    """Login or register a user via Telegram."""
    try:
        # Check if user exists
        user = await get_user_by_telegram_id(telegram_id)
        if user:
            return user
        
        # Create new user if not exists
        return await create_user(telegram_id=telegram_id, username=username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 