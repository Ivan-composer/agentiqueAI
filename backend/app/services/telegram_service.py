import os
import traceback
from telethon import TelegramClient
from telethon.errors import ChannelPrivateError, ChannelInvalidError
from telethon.sessions import StringSession, SQLiteSession
from dotenv import load_dotenv
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from the correct path
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

# Get environment variables with error checking
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')

if not API_ID or not API_HASH:
    logger.error("[TelegramService] Missing required Telegram API credentials!")
    logger.error(f"API_ID present: {bool(API_ID)}")
    logger.error(f"API_HASH present: {bool(API_HASH)}")
    raise ValueError("Missing required Telegram API credentials")

# Convert API_ID to integer
API_ID = int(API_ID)

# Device info to mimic MacBook Pro
DEVICE_MODEL = 'MacBook Pro'
SYSTEM_VERSION = 'macOS 11.5'
APP_VERSION = '9.3.2'  # Current Telegram macOS version
LANG_CODE = 'en'
SYSTEM_LANG_CODE = 'en'

# Use a persistent session file in a known location
SESSION_DIR = Path("sessions")
SESSION_FILE = SESSION_DIR / "agentique_server_session"

# Ensure session directory exists
SESSION_DIR.mkdir(exist_ok=True)

class TelegramService:
    _instance = None
    _client = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TelegramService, cls).__new__(cls)
        return cls._instance
    
    async def get_client(self):
        async with self._lock:  # Ensure thread-safe client initialization
            if not self._client:
                logger.info("[TelegramService] Initializing new client...")
                
                # Try to load from string session backup first
                try:
                    backup_file = SESSION_FILE.with_suffix('.backup')
                    if backup_file.exists():
                        with open(backup_file, 'r') as f:
                            session_str = f.read().strip()
                            if session_str:
                                self._client = TelegramClient(
                                    StringSession(session_str),
                                    API_ID,
                                    API_HASH,
                                    device_model=DEVICE_MODEL,
                                    system_version=SYSTEM_VERSION,
                                    app_version=APP_VERSION,
                                    lang_code=LANG_CODE,
                                    system_lang_code=SYSTEM_LANG_CODE,
                                    connection_retries=None
                                )
                except Exception as e:
                    logger.error(f"[TelegramService] Error loading backup session: {str(e)}")
                
                # If string session failed, use SQLite session
                if not self._client:
                    self._client = TelegramClient(
                        str(SESSION_FILE),
                        API_ID,
                        API_HASH,
                        device_model=DEVICE_MODEL,
                        system_version=SYSTEM_VERSION,
                        app_version=APP_VERSION,
                        lang_code=LANG_CODE,
                        system_lang_code=SYSTEM_LANG_CODE,
                        connection_retries=None
                    )
            
            if not self._client.is_connected():
                logger.info("[TelegramService] Connecting client...")
                await self._client.connect()
                
                if not await self._client.is_user_authorized():
                    logger.error("[TelegramService] Client not authorized!")
                    return None
                
                # Create a backup of the session
                try:
                    if isinstance(self._client.session, SQLiteSession):
                        # If using SQLite session, convert to string session for backup
                        session_str = StringSession.save(self._client.session)
                        with open(SESSION_FILE.with_suffix('.backup'), 'w') as f:
                            f.write(session_str)
                        logger.info("[TelegramService] Session backup created")
                except Exception as e:
                    logger.error(f"[TelegramService] Error creating session backup: {str(e)}")
            
            return self._client

    async def extract_channel_id(self, channel_link: str) -> str:
        """Extract channel ID from link."""
        logger.info(f"[TelegramService] Extracting channel ID from link: {channel_link}")
        try:
            # Remove https://t.me/ if present
            channel_id = channel_link.replace('https://t.me/', '')
            # Remove @ if present
            channel_id = channel_id.replace('@', '')
            logger.info(f"[TelegramService] Extracted channel ID: {channel_id}")
            return channel_id
        except Exception as e:
            logger.error(f"[TelegramService] Error extracting channel ID: {str(e)}")
            return None

    async def fetch_channel_messages(self, channel_link: str, limit: int = 100) -> list:
        """Fetch messages from a channel."""
            logger.info(f"\n[TelegramService] Starting to fetch messages from: {channel_link}")
            
        try:
            client = await self.get_client()
            if not client:
                logger.error("[TelegramService] Failed to get authorized client!")
                return []
            
            channel_id = await self.extract_channel_id(channel_link)
            if not channel_id:
                logger.error("[TelegramService] Failed to extract channel ID!")
                return []
                
            logger.info(f"[TelegramService] Fetching messages for channel: {channel_id}")
            
            # Get the channel entity first
            try:
                channel = await client.get_entity(channel_id)
                logger.info(f"[TelegramService] Found channel: {channel.title}")
            except Exception as e:
                logger.error(f"[TelegramService] Error getting channel entity: {str(e)}")
                return []
            
            messages = []
            message_count = 0
                    
            logger.info(f"[TelegramService] Starting to iterate through messages (limit: {limit})...")
            async for message in client.iter_messages(channel, limit=limit):
                message_count += 1
                if message and message.text:
                    messages.append({
                    'text': message.text,
                        'message_id': str(message.id),
                        'timestamp': message.date.isoformat(),
                        'link': f"https://t.me/{channel_id}/{message.id}"
                    })
                    if len(messages) % 10 == 0:
                        logger.info(f"[TelegramService] Processed {len(messages)} messages with text")
            
            logger.info(f"\n[TelegramService] Message processing summary:")
            logger.info(f"Total messages checked: {message_count}")
            logger.info(f"Messages with text: {len(messages)}")
                
            if messages:
                logger.info("\n[TelegramService] First message preview:")
                logger.info(f"ID: {messages[0]['message_id']}")
                logger.info(f"Text: {messages[0]['text'][:100]}...")
                
            return messages
            
        except Exception as e:
            logger.error(f"\n[TelegramService] Error fetching messages:")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}")
            traceback.print_exc()
            return []

    async def validate_channel(self, channel_link: str) -> bool:
        """Validate if a channel exists and is accessible."""
        logger.info(f"\n[TelegramService] Validating channel: {channel_link}")
            
        try:
            client = await self.get_client()
            if not client:
                logger.error("[TelegramService] Failed to get authorized client!")
                return False
                
            channel_id = await self.extract_channel_id(channel_link)
            if not channel_id:
                logger.error("[TelegramService] Failed to extract channel ID!")
                return False
                
            logger.info(f"[TelegramService] Attempting to get channel entity: {channel_id}")
            entity = await client.get_entity(channel_id)
            
            logger.info("[TelegramService] Channel validation successful!")
            return True
            
        except (ChannelPrivateError, ChannelInvalidError) as e:
            logger.error(f"[TelegramService] Channel validation failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"\n[TelegramService] Error validating channel:")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}")
            traceback.print_exc()
            return False
            
    async def init_client(self) -> bool:
        """Initialize and test the Telegram client."""
        logger.info("\n[TelegramService] Initializing Telegram client...")
        
        try:
            client = await self.get_client()
            if not client:
                return False
            
            # Check if we're authorized
            if not await client.is_user_authorized():
                logger.error("[TelegramService] Client not authorized! Please run the auth process.")
                return False
            
            # Test by trying to get our own user info
            me = await client.get_me()
            logger.info(f"[TelegramService] Connected as: {me.username if me else 'Unknown'}")
            
            logger.info("[TelegramService] Client initialized and authorized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"\n[TelegramService] Error initializing client:")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}")
            traceback.print_exc()
            return False
            
    async def check_auth(self) -> Dict[str, Any]:
        """Check authentication status"""
        try:
            client = await self.get_client()
            if not client:
                return {"authorized": False, "error": "Failed to initialize client"}
            
            if not await client.is_user_authorized():
                return {"authorized": False, "error": "Client not authorized"}
            
            me = await client.get_me()
            return {
                "authorized": True,
                "username": me.username if me else "Unknown",
                "phone": me.phone if me else None
            }
            
        except Exception as e:
            logger.error(f"[TelegramService] Error checking auth: {str(e)}")
            return {"authorized": False, "error": str(e)}

# Create a singleton instance
telegram_service = TelegramService() 