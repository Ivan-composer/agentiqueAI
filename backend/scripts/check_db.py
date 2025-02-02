"""
Script to check database tables and their contents.
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.db_service import supabase
from app.utils.logger import logger

async def check_database():
    """Check the contents of database tables."""
    try:
        # Check users
        users = supabase.table("users").select("*").execute()
        print("\nUsers:")
        print(users.data)

        # Check agents
        agents = supabase.table("agents").select("*").execute()
        print("\nAgents:")
        print(agents.data)

    except Exception as e:
        print(f"Error checking database: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(check_database()) 