from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
import os
from dotenv import load_dotenv
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_channel_access():
    # Load environment variables
    load_dotenv()
    
    # Get credentials
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    
    logger.info("Starting Telegram client...")
    client = TelegramClient('test_session', api_id, api_hash)
    
    try:
        await client.start(phone=phone)
        logger.info("Successfully connected to Telegram")
        
        # Test channels
        channels = ['@serafimcloud', '@tatespeech', '@startupoftheday']
        
        for channel_username in channels:
            try:
                logger.info(f"\nTesting channel: {channel_username}")
                
                # Get the channel entity
                channel = await client.get_entity(channel_username)
                logger.info(f"✓ Successfully got channel entity")
                
                # Try to get channel info
                full_channel = await client(GetFullChannelRequest(channel))
                logger.info(f"✓ Channel info: {full_channel.chats[0].title} (id: {channel.id})")
                logger.info(f"✓ Participant count: {full_channel.full_chat.participants_count}")
                
                # Try to get messages
                messages = await client.get_messages(channel, limit=5)
                if messages:
                    logger.info(f"✓ Successfully retrieved {len(messages)} messages")
                    for msg in messages:
                        logger.info(f"  - Message ID {msg.id}: {msg.message[:50]}...")
                else:
                    logger.warning("✗ No messages found")
                
            except Exception as e:
                logger.error(f"Error with channel {channel_username}: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        await client.disconnect()
        logger.info("Disconnected from Telegram")

if __name__ == '__main__':
    asyncio.run(test_channel_access()) 