"""
Script to check if all required environment variables are set.
"""
import os
from dotenv import load_dotenv

def check_env_vars():
    """Check if all required environment variables are set."""
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "OPENAI_API_KEY",
        "PINECONE_API_KEY",
        "PINECONE_ENVIRONMENT",
        "TELEGRAM_API_ID",
        "TELEGRAM_API_HASH",
        "TELEGRAM_PHONE"
    ]

    load_dotenv()
    
    print("\nChecking environment variables:")
    all_present = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # For sensitive values, only show first few characters
            if any(sensitive in var.lower() for sensitive in ["key", "hash", "password", "secret"]):
                display_value = f"{value[:8]}..."
            else:
                display_value = value
            print(f"✅ {var} = {display_value}")
        else:
            print(f"❌ {var} is not set")
            all_present = False
    
    if all_present:
        print("\nAll required environment variables are set! 🎉")
    else:
        print("\n⚠️ Some required environment variables are missing!")

if __name__ == "__main__":
    check_env_vars() 