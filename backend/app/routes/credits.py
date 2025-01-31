"""
credits.py: Routes for managing user credits.
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from app.services.payment_service import add_credits, deduct_credits

router = APIRouter(prefix="/credits", tags=["credits"])

@router.post("/add/{user_id}")
async def add_user_credits(user_id: str, amount: Dict[str, int]) -> Dict[str, Any]:
    """
    Add credits to a user's balance.
    
    Args:
        user_id: The user's ID
        amount: Dictionary containing the amount of credits to add
    
    Returns:
        Dict with new balance
    """
    if "amount" not in amount:
        raise HTTPException(status_code=400, detail="Missing amount field in request body")
    
    return await add_credits(user_id, amount["amount"], reason="manual_add")

@router.post("/deduct/{user_id}")
async def deduct_user_credits(user_id: str, amount: Dict[str, int]) -> Dict[str, Any]:
    """
    Deduct credits from a user's balance.
    
    Args:
        user_id: The user's ID
        amount: Dictionary containing the amount of credits to deduct
    
    Returns:
        Dict with new balance
    """
    if "amount" not in amount:
        raise HTTPException(status_code=400, detail="Missing amount field in request body")
    
    return await deduct_credits(user_id, amount["amount"], reason="manual_deduct") 