"""
Telegram service for channel content ingestion.
Handles authentication, channel access, and message retrieval with rate limiting.
"""
import os
from typing import List, Dict, Any, Optional
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Message
from telethon.tl.functions.channels import GetFullChannelRequest
from datetime import datetime, timedelta
import asyncio
from app.utils.logger import logger
from app.utils.errors import TelegramError

# Device info to match MacBook Pro to avoid conflicts with personal sessions
DEVICE_MODEL = "MacBook Pro"
SYSTEM_VERSION = "macOS 12.6"
APP_VERSION = "9.3.3"
LANG_CODE = "en"
SYSTEM_LANG_CODE = "en"

# Default session name for consistency
DEFAULT_SESSION_NAME = "agentique_bot"

# Default message limit to avoid overloading
DEFAULT_MESSAGE_LIMIT = 50

class TelegramService:
    def __init__(self, session: Optional[str] = None):
        """
        Initialize Telegram client with API credentials.
        
        Args:
            session: Optional session string. If not provided, uses default bot session.
            
        Raises:
            TelegramError: If required credentials are missing
        """
        self.api_id = int(os.getenv("TELEGRAM_API_ID", "0"))
        self.api_hash = os.getenv("TELEGRAM_API_HASH", "")
        self.phone = os.getenv("TELEGRAM_PHONE", "")
        
        if not all([self.api_id, self.api_hash, self.phone]):
            logger.error("Missing Telegram credentials in environment variables")
            raise TelegramError("initialization", {"error": "Missing required credentials"})
        
        # Get the session string from environment if available
        session_string = os.getenv("TELEGRAM_SESSION_STRING")
        
        if session_string:
            logger.info("Using provided session string")
            self.client = TelegramClient(
                StringSession(session_string),
                self.api_id,
                self.api_hash,
                device_model=DEVICE_MODEL,
                system_version=SYSTEM_VERSION,
                app_version=APP_VERSION,
                lang_code=LANG_CODE,
                system_lang_code=SYSTEM_LANG_CODE
            )
        else:
            # Get the absolute path to the backend directory
            backend_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            
            # Ensure sessions directory exists in backend root
            sessions_dir = os.path.join(backend_dir, "sessions")
            os.makedirs(sessions_dir, exist_ok=True)
            
            # Use absolute path for session file
            session_path = os.path.join(sessions_dir, DEFAULT_SESSION_NAME)
            logger.info("Using session file: %s", session_path)
            
            self.client = TelegramClient(
                session_path,
                self.api_id,
                self.api_hash,
                device_model=DEVICE_MODEL,
                system_version=SYSTEM_VERSION,
                app_version=APP_VERSION,
                lang_code=LANG_CODE,
                system_lang_code=SYSTEM_LANG_CODE
            )

    async def connect(self) -> None:
        """
        Connect to Telegram and ensure authorization.
        
        Raises:
            TelegramError: If connection fails or no valid session exists
        """
        try:
            if not self.client.is_connected():
                logger.info("Connecting to Telegram...")
                await self.client.connect()
                
                if not await self.client.is_user_authorized():
                    logger.error("No valid session found. Please run telegram_auth.py first to create a session.")
                    raise TelegramError("authentication", {"error": "No valid session found"})
                
                logger.info("Successfully connected using existing session")
        except Exception as e:
            logger.error("Failed to connect to Telegram: %s", str(e))
            raise TelegramError("connection", {"error": str(e)})

    async def verify_code(self, code: str) -> bool:
        """
        Verify the authentication code received via SMS/Telegram.
        
        Args:
            code: The verification code received
            
        Returns:
            bool: True if verification successful
            
        Raises:
            TelegramError: If verification fails
        """
        try:
            logger.info("Verifying code for phone: %s", self.phone)
            await self.client.sign_in(self.phone, code)
            return True
        except Exception as e:
            logger.error("Failed to verify code: %s", str(e))
            raise TelegramError("verification", {"error": str(e)})

    async def get_channel_messages(
        self,
        channel_link: str,
        limit: Optional[int] = None,
        min_id: Optional[int] = None,
        offset_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve messages from a Telegram channel with support for partial ingestion.
        
        Args:
            channel_link: The channel's username or invite link
            limit: Maximum number of messages to retrieve (defaults to DEFAULT_MESSAGE_LIMIT)
            min_id: Minimum message ID to retrieve (for partial ingestion)
            offset_date: Only retrieve messages after this date
            
        Returns:
            List of message dictionaries with text and metadata
            
        Raises:
            TelegramError: If message retrieval fails
        """
        try:
            await self.connect()
            
            # Clean up channel link
            channel_link = channel_link.strip()
            if channel_link.startswith('https://t.me/'):
                channel_link = channel_link[13:]  # Remove https://t.me/
            elif not channel_link.startswith('@'):
                channel_link = f"@{channel_link}"  # Add @ if not present
            
            # Remove any trailing slashes
            channel_link = channel_link.rstrip('/')
            
            logger.info("Attempting to fetch messages from channel: %s", channel_link)
            
            # Try to get the channel entity
            try:
                logger.debug("Getting entity for channel: %s", channel_link)
                channel = await self.client.get_entity(channel_link)
            except Exception as e:
                logger.error("Failed to get channel entity: %s", str(e))
                raise TelegramError("channel_access", {
                    "error": str(e),
                    "channel": channel_link,
                    "details": "Channel might be private or not exist"
                })

            if not channel:
                raise TelegramError("channel_access", {
                    "error": "Could not get channel entity",
                    "channel": channel_link,
                    "details": "Channel might be private or not exist"
                })
            
            logger.info("Successfully got channel entity, fetching messages...")
            
            # Prepare parameters for message retrieval
            kwargs = {
                "limit": min(limit if limit else DEFAULT_MESSAGE_LIMIT, DEFAULT_MESSAGE_LIMIT),  # Never exceed DEFAULT_MESSAGE_LIMIT
                "reverse": False  # Get newest messages first
            }
            if min_id:
                kwargs["min_id"] = min_id
            if offset_date:
                kwargs["offset_date"] = offset_date
            
            logger.info("Fetching up to %d messages from channel", kwargs["limit"])
            
            messages = []
            message_count = 0
            last_message_time = None
            
            # Use get_messages instead of iter_messages for a fixed limit
            telegram_messages = await self.client.get_messages(channel, **kwargs)
            
            for message in telegram_messages:
                if not isinstance(message, Message) or not message.text:
                    continue
                
                # Format message data
                message_data = {
                    "id": message.id,
                    "text": message.text,
                    "date": message.date.isoformat(),
                    "link": f"{channel_link}/{message.id}",
                    "views": getattr(message, "views", 0),
                    "forwards": getattr(message, "forwards", 0)
                }
                messages.append(message_data)
                message_count += 1
                last_message_time = message.date
            
            if not messages:
                logger.warning("No messages found in channel %s", channel_link)
            else:
                logger.info("Successfully retrieved %d messages from %s", len(messages), channel_link)
            
            return messages
            
        except TelegramError:
            raise
        except Exception as e:
            logger.error("Failed to retrieve messages from %s: %s", channel_link, str(e))
            raise TelegramError("message_retrieval", {"error": str(e), "channel": channel_link})

    async def disconnect(self) -> None:
        """
        Safely disconnect from Telegram.
        
        Raises:
            TelegramError: If disconnection fails
        """
        try:
            if self.client.is_connected():
                logger.info("Disconnecting from Telegram")
                await self.client.disconnect()
        except Exception as e:
            logger.error("Failed to disconnect from Telegram: %s", str(e))
            raise TelegramError("disconnection", {"error": str(e)})

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()

    async def get_channel_info(self, channel_link: str) -> Dict[str, Any]:
        """
        Get information about a Telegram channel.
        
        Args:
            channel_link: The channel link or username
            
        Returns:
            Dict containing channel info (title, id, etc.)
            
        Raises:
            TelegramError: If channel cannot be accessed or other errors occur
        """
        try:
            # Get the channel entity
            channel = await self.client.get_entity(channel_link)
            
            # Get full channel info
            full_channel = await self.client(GetFullChannelRequest(channel))
            
            return {
                "title": full_channel.chats[0].title,
                "id": channel.id,
                "participant_count": full_channel.full_chat.participants_count
            }
            
        except Exception as e:
            logger.error("Failed to get channel info for %s: %s", channel_link, str(e))
            raise TelegramError("channel_access", {"error": str(e), "channel": channel_link})