"""
Pytest configuration and fixtures.
"""
import os
import pytest
import uuid
import asyncio
from httpx import AsyncClient
from app.services.db_service import supabase
from main import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client():
    """Create a test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def test_user():
    """Create a test user for testing."""
    # Generate a unique telegram_id using uuid4
    telegram_id = str(uuid.uuid4().int)[:15]  # Take first 15 digits for telegram_id
    
    # Create test user with unique telegram_id
    user = supabase.table('users').insert({
        'telegram_id': telegram_id,
        'credits_balance': 0
    }).execute()
    
    user_id = user.data[0]['id']
    
    # Verify user exists before proceeding
    verification = supabase.table('users').select("*").eq('id', user_id).execute()
    assert verification.data, "Test user was not created properly"
    
    yield user_id
    
    # Cleanup: Delete transactions first, then delete the user
    try:
        supabase.table('transactions').delete().eq('user_id', user_id).execute()
    except Exception as e:
        print(f"Error deleting transactions: {e}")
    
    try:
        supabase.table('users').delete().eq('id', user_id).execute()
    except Exception as e:
        print(f"Error deleting user: {e}") 