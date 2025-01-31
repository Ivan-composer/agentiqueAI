"""
Test script to verify Telegram channel ingestion.
Tests partial ingestion and rate limiting with a real channel.
"""
import asyncio
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.telegram_service import TelegramService
from app.utils.logger import logger

async def test_channel_ingestion():
    """Test different ingestion scenarios with a test channel."""
    service = None
    try:
        # Initialize service with our persistent session
        service = TelegramService()
        await service.connect()
        
        channel = "johndoetest12"
        logger.info(f"Testing channel ingestion from: {channel}")
        
        # Test 1: Get last 5 messages
        logger.info("\n=== Test 1: Last 5 messages ===")
        messages = await service.get_channel_messages(channel, limit=5)
        logger.info(f"Retrieved {len(messages)} messages")
        for msg in messages:
            logger.info(f"Message {msg['id']} from {msg['date']}: {msg['text'][:100]}...")
        
        if messages:
            # Test 2: Get messages after the oldest message we just retrieved
            oldest_msg_id = min(msg['id'] for msg in messages)
            logger.info(f"\n=== Test 2: Messages after ID {oldest_msg_id} ===")
            older_messages = await service.get_channel_messages(
                channel,
                min_id=oldest_msg_id,
                limit=3
            )
            logger.info(f"Retrieved {len(older_messages)} messages after ID {oldest_msg_id}")
        
        # Test 3: Get messages from last week
        logger.info("\n=== Test 3: Last week's messages ===")
        week_ago = datetime.now() - timedelta(days=7)
        recent_messages = await service.get_channel_messages(
            channel,
            offset_date=week_ago,
            limit=5
        )
        logger.info(f"Retrieved {len(recent_messages)} messages from last week")
        
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")
        raise
    finally:
        if service:
            await service.disconnect()

if __name__ == "__main__":
    logger.info("Starting channel ingestion tests...")
    asyncio.run(test_channel_ingestion()) 