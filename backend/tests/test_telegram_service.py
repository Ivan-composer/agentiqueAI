"""
Tests for Telegram service.
"""
import pytest
from datetime import datetime, timedelta
from app.services.telegram_service import TelegramService

@pytest.fixture
async def telegram_service():
    """Create a Telegram service instance for testing using the main session."""
    service = TelegramService()  # Use default session (phone number)
    await service.connect()
    yield service
    await service.disconnect()

@pytest.mark.asyncio
async def test_telegram_initialization(telegram_service):
    """Test Telegram service initialization."""
    assert telegram_service.api_id != 0
    assert telegram_service.api_hash != ""
    assert telegram_service.phone != ""

@pytest.mark.asyncio
async def test_channel_message_retrieval(telegram_service):
    """Test retrieving messages from a public channel."""
    # Use a known public channel for testing
    channel_link = "telegram"  # Telegram's official channel
    
    # Test partial ingestion with limit
    messages = await telegram_service.get_channel_messages(
        channel_link=channel_link,
        limit=5  # Only get 5 messages for testing
    )
    assert isinstance(messages, list)
    assert len(messages) <= 5
    
    if messages:
        message = messages[0]
        assert "id" in message
        assert "text" in message
        assert "date" in message
        assert "link" in message
        assert "views" in message
        assert "forwards" in message

@pytest.mark.asyncio
async def test_partial_ingestion_with_date(telegram_service):
    """Test partial ingestion with date filtering."""
    channel_link = "telegram"
    offset_date = datetime.now() - timedelta(days=7)  # Last week's messages
    
    messages = await telegram_service.get_channel_messages(
        channel_link=channel_link,
        offset_date=offset_date,
        limit=5
    )
    
    if messages:
        for message in messages:
            message_date = datetime.fromisoformat(message["date"])
            assert message_date >= offset_date

@pytest.mark.asyncio
async def test_partial_ingestion_with_min_id(telegram_service):
    """Test partial ingestion with minimum message ID."""
    channel_link = "telegram"
    
    # First get some messages to find a min_id
    initial_messages = await telegram_service.get_channel_messages(
        channel_link=channel_link,
        limit=1
    )
    
    if initial_messages:
        min_id = initial_messages[0]["id"]
        
        # Then get messages after that ID
        messages = await telegram_service.get_channel_messages(
            channel_link=channel_link,
            min_id=min_id,
            limit=5
        )
        
        if messages:
            for message in messages:
                assert message["id"] >= min_id 