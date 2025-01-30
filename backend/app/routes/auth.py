from fastapi import APIRouter, HTTPException
from ..services import db_service

router = APIRouter()

@router.post("/telegram")
async def telegram_auth(telegram_id: str, username: str = None):
    """Authenticate user with Telegram ID"""
    # Check if user exists
    user = await db_service.get_user_by_telegram_id(telegram_id)
    
    if not user:
        # Create new user if doesn't exist
        user = await db_service.create_user(telegram_id, username)
        if not user:
            raise HTTPException(status_code=500, detail="Failed to create user")
    
    return {"user": user}

@router.get("/me/{telegram_id}")
async def get_current_user(telegram_id: str):
    """Get current authenticated user"""
    user = await db_service.get_user_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 