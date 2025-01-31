"""
Tests for database operations.
"""
import pytest
from app.services.db_service import (
    create_user,
    get_user_by_telegram_id,
    create_agent,
    get_agent_by_id,
    save_chat_message,
    record_transaction,
    supabase
)

async def cleanup_test_data():
    """Clean up test data before each test."""
    try:
        # Use RPC calls to clean up test data
        supabase.rpc('cleanup_test_users').execute()
        supabase.rpc('cleanup_test_agents').execute()
        supabase.rpc('cleanup_test_chat_messages').execute()
        supabase.rpc('cleanup_test_transactions').execute()
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

@pytest.fixture(autouse=True)
async def setup_and_cleanup():
    """Setup and cleanup before and after each test."""
    try:
        await cleanup_test_data()
        yield
        await cleanup_test_data()
    except Exception as e:
        print(f"Error in setup/cleanup: {str(e)}")

@pytest.mark.asyncio
async def test_user_operations():
    """Test basic user operations."""
    # Create a test user
    test_telegram_id = f"test_user_{pytest.id_generator()}"
    test_username = "test_user"
    
    # Create user
    user = await create_user(test_telegram_id, test_username)
    assert user is not None
    assert user["telegram_id"] == test_telegram_id
    assert user["username"] == test_username
    
    # Retrieve user
    retrieved_user = await get_user_by_telegram_id(test_telegram_id)
    assert retrieved_user is not None
    assert retrieved_user["telegram_id"] == test_telegram_id

@pytest.mark.asyncio
async def test_agent_creation():
    """Test agent creation."""
    # First create a test user
    test_telegram_id = f"test_owner_{pytest.id_generator()}"
    user = await create_user(test_telegram_id, "test_owner")
    
    # Create an agent
    agent = await create_agent(
        owner_id=user["id"],
        expert_name="Test Expert",
        prompt_template="Test template"
    )
    assert agent is not None
    assert agent["owner_id"] == user["id"]
    assert agent["expert_name"] == "Test Expert"

    # Get agent
    retrieved_agent = await get_agent_by_id(agent["id"])
    assert retrieved_agent is not None
    assert retrieved_agent["id"] == agent["id"]

@pytest.mark.asyncio
async def test_chat_message():
    """Test chat message creation."""
    # Create test user and agent first
    test_telegram_id = f"test_chat_{pytest.id_generator()}"
    user = await create_user(test_telegram_id, "test_chat_user")
    agent = await create_agent(user["id"], "Test Chat Expert", "Test template")
    
    # Save a chat message
    message = await save_chat_message(
        agent_id=agent["id"],
        user_id=user["id"],
        role="user",
        content="Test message"
    )
    assert message is not None
    assert message["agent_id"] == agent["id"]
    assert message["user_id"] == user["id"]
    assert message["content"] == "Test message"

@pytest.mark.asyncio
async def test_transaction():
    """Test transaction recording."""
    # Create test user first
    test_telegram_id = f"test_trans_{pytest.id_generator()}"
    user = await create_user(test_telegram_id, "test_trans_user")
    
    # Record a transaction
    transaction = await record_transaction(
        user_id=user["id"],
        credits_change=100,
        reason="Test transaction"
    )
    assert transaction is not None
    assert transaction["user_id"] == user["id"]
    assert transaction["credits_change"] == 100
    assert transaction["reason"] == "Test transaction" 