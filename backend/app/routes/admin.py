"""
admin.py: Admin-only routes for managing the platform.
"""
import os
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header
from app.services.payment_service import add_credits

router = APIRouter(tags=["admin"])

ADMIN_KEY = os.getenv("ADMIN_KEY", "test_admin_key")

async def verify_admin(admin_key: Optional[str] = None):
    """Verify admin access using admin key from headers."""
    if not admin_key:
        raise HTTPException(status_code=403, detail="Missing admin key")
    if admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")

@router.post("/credits/topup/{user_id}")
async def admin_topup(
    user_id: str,
    amount: Dict[str, int],
    admin_key: Optional[str] = Header(None, alias="X-Admin-Key")
) -> Dict[str, Any]:
    """
    Top up a user's credits. Admin-only endpoint.
    
    Args:
        user_id: The user's ID to top up
        amount: Dictionary containing the amount of credits to add
        admin_key: Admin API key for authorization
    
    Returns:
        Dict with new balance
        
    Raises:
        HTTPException: If admin key is missing or invalid (403) or user not found (404)
    """
    # Verify admin access
    await verify_admin(admin_key)
    
    # Check if amount field exists
    if "amount" not in amount:
        raise HTTPException(status_code=400, detail="Missing amount field in request body")
    
    # Add credits to user's balance
    return await add_credits(user_id, amount["amount"], reason="admin_topup") 