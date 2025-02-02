"""
Script to delete all agents except TateB.
"""
import os
import sys
import logging
from dotenv import load_dotenv
from supabase import create_client, Client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agentique")

# Load environment variables
load_dotenv()

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")
supabase: Client = create_client(url, key)

logger.info("Initializing Supabase client with URL: %s", url[:30])

try:
    # Get all agents
    response = supabase.table("agents").select("*").execute()
    agents = response.data

    for agent in agents:
        agent_id = agent["id"]
        expert_name = agent["expert_name"]
        
        # Skip TateB agent
        if expert_name == "TateB":
            logger.info(f"Skipping agent {agent_id} (TateB)")
            continue
            
        logger.info(f"Deleting agent {agent_id} ({expert_name})")
        
        try:
            # First delete associated chat messages
            logger.debug(f"Deleting chat messages for agent: {agent_id}")
            supabase.table("chat_messages").delete().eq("agent_id", agent_id).execute()
            
            # Then delete the agent
            logger.debug(f"Deleting agent with id: {agent_id}")
            response = supabase.table("agents").delete().eq("id", agent_id).execute()
            logger.info(f"Successfully deleted agent with id: {agent_id}")
            
        except Exception as e:
            logger.error(f"Failed to delete agent with id: {agent_id} - {e.args[0]}")
            continue

except Exception as e:
    logger.error(f"Error deleting agents: {e.args[0]}")
    sys.exit(1)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(delete_agents()) 