"""
Script to authenticate with Telegram and create a session file.
This only needs to be run once to create a valid session.
"""
import os
import sys
import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import *
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get credentials from environment variables
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE = os.getenv("TELEGRAM_PHONE")

if not all([API_ID, API_HASH, PHONE]):
    logger.error("Missing required environment variables.")
    print("Error: Missing required environment variables.")
    print("Please ensure TELEGRAM_API_ID, TELEGRAM_API_HASH, and TELEGRAM_PHONE are set.")
    sys.exit(1)

# Convert API_ID to integer
API_ID = int(API_ID)

# Device info to match MacBook Pro
DEVICE_MODEL = "MacBook Pro"
SYSTEM_VERSION = "macOS 12.6"
APP_VERSION = "9.3.3"
LANG_CODE = "en"
SYSTEM_LANG_CODE = "en"

# Default session name for consistency
DEFAULT_SESSION_NAME = "agentique_bot"

# Get the absolute path to the backend directory
BACKEND_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Ensure sessions directory exists in backend root
SESSIONS_DIR = os.path.join(BACKEND_DIR, "sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)

# Use absolute path for session file
SESSION_FILE = os.path.join(SESSIONS_DIR, DEFAULT_SESSION_NAME)

async def main():
    """Run the authentication flow."""
    logger.info("Starting Telegram authentication process...")
    print("\nStarting Telegram authentication process...")
    
    # Create the client with device info
    client = TelegramClient(
        SESSION_FILE,
        API_ID,
        API_HASH,
        device_model=DEVICE_MODEL,
        system_version=SYSTEM_VERSION,
        app_version=APP_VERSION,
        lang_code=LANG_CODE,
        system_lang_code=SYSTEM_LANG_CODE
    )
    
    try:
        # Start the client
        logger.info("Connecting to Telegram...")
        print("Connecting to Telegram...")
        await client.connect()
        
        # Check if already authorized
        if await client.is_user_authorized():
            logger.info("Already authenticated!")
            print("\nAlready authenticated!")
            return
        
        # Send code request
        logger.info("Sending code request...")
        print("\nSending code request...")
        await client.send_code_request(PHONE)
        
        # Get the code from user input
        code = input("\nEnter the code you received: ")
        
        try:
            # Sign in with the code
            logger.info("Attempting to sign in...")
            print("\nAttempting to sign in...")
            await client.sign_in(PHONE, code)
            logger.info("Successfully authenticated!")
            print("\nSuccessfully authenticated!")
            
        except PhoneCodeInvalidError:
            logger.error("Invalid code provided")
            print("\nError: The code you entered is invalid.")
            sys.exit(1)
            
        except SessionPasswordNeededError:
            # 2FA is enabled
            logger.info("2FA is enabled, requesting password")
            print("\n2FA is enabled. Please enter your password:")
            password = input("Password: ")
            
            try:
                await client.sign_in(password=password)
                logger.info("Successfully authenticated with 2FA!")
                print("\nSuccessfully authenticated with 2FA!")
            except PasswordHashInvalidError:
                logger.error("Invalid 2FA password")
                print("\nError: Invalid 2FA password")
                sys.exit(1)
                
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        print(f"\nAuthentication failed: {str(e)}")
        # Clean up invalid session file
        if os.path.exists(f"{SESSION_FILE}.session"):
            os.remove(f"{SESSION_FILE}.session")
        sys.exit(1)
        
    finally:
        if 'client' in locals():
            await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAuthentication cancelled by user.")
        sys.exit(0) 