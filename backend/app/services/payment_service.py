"""
payment_service.py: Handles credit operations and transactions.
"""
from typing import Dict, Any
from app.services.db_service import supabase
from fastapi import HTTPException
from app.utils.errors import InsufficientCreditsError

async def deduct_credits(user_id: str, amount: int, reason: str) -> Dict[str, Any]:
    """
    Deduct credits from user balance and record transaction.
    
    Args:
        user_id: The user's ID
        amount: Number of credits to deduct
        reason: Reason for deduction ('chat', 'search', or 'comment')
    
    Returns:
        Dict with updated credits balance
    
    Raises:
        HTTPException: If user not found (404)
        InsufficientCreditsError: If user has insufficient credits
    """
    # Get current user balance
    user = supabase.table('users').select('credits_balance').eq('id', user_id).single().execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    balance = user.data['credits_balance']
    if balance < amount:
        raise InsufficientCreditsError(current_balance=balance, required_amount=amount)
    
    # Update balance
    new_balance = balance - amount
    supabase.table('users').update({'credits_balance': new_balance}).eq('id', user_id).execute()
    
    # Record transaction
    supabase.table('transactions').insert({
        'user_id': user_id,
        'credits_change': -amount,
        'reason': reason
    }).execute()
    
    return {"credits_balance": new_balance}

async def add_credits(user_id: str, amount: int, reason: str = "top_up") -> Dict[str, Any]:
    """
    Add credits to user balance and record transaction.
    
    Args:
        user_id: The user's ID
        amount: Number of credits to add
        reason: Reason for addition (default: 'top_up')
    
    Returns:
        Dict with updated credits balance
        
    Raises:
        HTTPException: If user not found (404)
    """
    # Get current user balance
    user = supabase.table('users').select('credits_balance').eq('id', user_id).single().execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update balance
    new_balance = user.data['credits_balance'] + amount
    supabase.table('users').update({'credits_balance': new_balance}).eq('id', user_id).execute()
    
    # Record transaction
    supabase.table('transactions').insert({
        'user_id': user_id,
        'credits_change': amount,
        'reason': reason
    }).execute()
    
    return {"credits_balance": new_balance} 