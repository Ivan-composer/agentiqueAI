"""
One-time authentication script for Telegram.
This script only needs to be run ONCE to create a persistent session file.
After running this successfully, the session file will be reused automatically.
"""
import os
import asyncio
from telethon import TelegramClient
from app.utils.logger import logger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Device info to match MacBook Pro to avoid conflicts with personal sessions
DEVICE_MODEL = "MacBook Pro"
SYSTEM_VERSION = "macOS 12.6"
APP_VERSION = "9.3.3"
LANG_CODE = "en"
SYSTEM_LANG_CODE = "en"

# Get the absolute path to the sessions directory
SESSIONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sessions"))

async def authenticate():
    """
    Interactive one-time authentication with Telegram.
    Creates a persistent session file that will be reused for all future connections.
    """
    try:
        # Get credentials from environment
        api_id = int(os.getenv("TELEGRAM_API_ID", "0"))
        api_hash = os.getenv("TELEGRAM_API_HASH", "")
        phone = os.getenv("TELEGRAM_PHONE", "")
        
        print("\n=== One-Time Telegram Authentication ===")
        print("This script will create a persistent session file.")
        print("You only need to run this ONCE. The session will be reused automatically.\n")
        
        print(f"Using credentials:")
        print(f"API ID: {api_id}")
        print(f"API Hash: {api_hash[:4]}...{api_hash[-4:]}")
        print(f"Phone: {phone}")
        
        if not all([api_id, api_hash, phone]):
            logger.error("Missing Telegram credentials in environment variables")
            print("Please set TELEGRAM_API_ID, TELEGRAM_API_HASH, and TELEGRAM_PHONE environment variables")
            return
        
        # Ensure sessions directory exists
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        session_file = os.path.join(SESSIONS_DIR, phone)
        
        if os.path.exists(f"{session_file}.session"):
            print(f"\nSession file already exists at: {session_file}.session")
            print("If you need to re-authenticate, please delete this file first.")
            return
            
        print(f"\nWill create new session file at: {session_file}.session")
        
        # Create client
        client = TelegramClient(
            session_file,
            api_id,
            api_hash,
            device_model=DEVICE_MODEL,
            system_version=SYSTEM_VERSION,
            app_version=APP_VERSION,
            lang_code=LANG_CODE,
            system_lang_code=SYSTEM_LANG_CODE
        )
        
        print("\nConnecting to Telegram...")
        logger.info("Starting one-time Telegram authentication process...")
        await client.connect()
        
        if not await client.is_user_authorized():
            print("\nNot authorized. Requesting verification code...")
            logger.info("Not authorized, sending code request...")
            sent = await client.send_code_request(phone)
            print(f"Code type: {sent.type}")
            
            # Get the verification code from user input
            verification_code = input("\nEnter the verification code sent to your Telegram: ")
            
            try:
                # Try to sign in
                print("\nAttempting to sign in...")
                await client.sign_in(phone, verification_code)
                logger.info("Successfully authenticated!")
                print("\nAuthentication successful!")
                print(f"Created persistent session file at: {session_file}.session")
                print("This file will be reused automatically for all future connections.")
                
            except Exception as e:
                if "2FA" in str(e) or "password" in str(e).lower():
                    print("\n2FA is enabled. Please enter your password.")
                    password = input("Enter your 2FA password: ")
                    await client.sign_in(password=password)
                    logger.info("Successfully authenticated with 2FA!")
                    print("\nAuthentication successful!")
                    print(f"Created persistent session file at: {session_file}.session")
                    print("This file will be reused automatically for all future connections.")
                else:
                    raise e
        else:
            logger.info("Already authorized!")
            print("\nAlready authenticated! Session file exists and is valid.")
            
    except Exception as e:
        logger.error("Authentication failed: %s", str(e))
        print(f"\nAuthentication failed: {str(e)}")
        if os.path.exists(f"{session_file}.session"):
            print(f"\nRemoving invalid session file: {session_file}.session")
            os.remove(f"{session_file}.session")
    
    finally:
        if 'client' in locals():
            await client.disconnect()
            print("\nDisconnected from Telegram.")

if __name__ == "__main__":
    print("Starting one-time Telegram authentication process...")
    asyncio.run(authenticate()) 