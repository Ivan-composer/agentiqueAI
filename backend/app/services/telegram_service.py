"""
Telegram service for channel content ingestion.
Handles authentication, channel access, and message retrieval with rate limiting.
"""
import os
from typing import List, Dict, Any, Optional
from telethon import TelegramClient
from telethon.tl.types import Message
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

class TelegramService:
    def __init__(self, session: Optional[str] = None):
        """
        Initialize Telegram client with API credentials.
        
        Args:
            session: Optional custom session name. If not provided, uses phone number.
            
        Raises:
            TelegramError: If required credentials are missing
        """
        self.api_id = int(os.getenv("TELEGRAM_API_ID", "0"))
        self.api_hash = os.getenv("TELEGRAM_API_HASH", "")
        self.phone = os.getenv("TELEGRAM_PHONE", "")
        
        if not all([self.api_id, self.api_hash, self.phone]):
            logger.error("Missing Telegram credentials in environment variables")
            raise TelegramError("initialization", {"error": "Missing required credentials"})
        
        # Use custom session name if provided, otherwise use phone number
        session_name = session if session else self.phone
        
        # Ensure sessions directory exists
        os.makedirs("sessions", exist_ok=True)
        
        # Use absolute path for session file
        session_path = os.path.abspath(os.path.join("sessions", session_name))
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
            limit: Maximum number of messages to retrieve
            min_id: Minimum message ID to retrieve (for partial ingestion)
            offset_date: Only retrieve messages after this date
            
        Returns:
            List of message dictionaries with text and metadata
            
        Raises:
            TelegramError: If message retrieval fails
        """
        try:
            await self.connect()
            
            logger.info("Fetching messages from channel: %s", channel_link)
            channel = await self.client.get_entity(channel_link)
            
            # Prepare parameters for message retrieval
            kwargs = {
                "limit": limit,
                "reverse": True  # Get oldest messages first
            }
            if min_id:
                kwargs["min_id"] = min_id
            if offset_date:
                kwargs["offset_date"] = offset_date
            
            messages = []
            message_count = 0
            last_message_time = None
            
            async for message in self.client.iter_messages(channel, **kwargs):
                if not isinstance(message, Message) or not message.text:
                    continue
                
                # Add rate limiting delay every 100 messages
                if message_count > 0 and message_count % 100 == 0:
                    logger.debug("Rate limiting delay after %d messages", message_count)
                    await asyncio.sleep(2)  # 2 second delay every 100 messages
                
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
                
                # Log progress periodically
                if message_count % 500 == 0:
                    logger.info("Retrieved %d messages from %s", message_count, channel_link)
            
            logger.info("Successfully retrieved %d messages from %s", len(messages), channel_link)
            return messages
            
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