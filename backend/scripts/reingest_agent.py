"""
Script to re-ingest content for a specific agent.
"""
import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Print environment variables for debugging
logger.info("Environment variables:")
logger.info("OPENAI_API_KEY: %s", os.getenv("OPENAI_API_KEY"))
logger.info("PINECONE_API_KEY: %s", os.getenv("PINECONE_API_KEY"))
logger.info("PINECONE_ENV: %s", os.getenv("PINECONE_ENV"))
logger.info("TELEGRAM_API_ID: %s", os.getenv("TELEGRAM_API_ID"))

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.telegram_service import TelegramService
from app.services.openai_service import generate_embedding
from app.services.pinecone_service import upsert_vectors
from uuid import uuid4

# Constants
AGENT_ID = "32fa1961-eb7c-4672-b1da-f91aa272b366"  # serafim.eth
CHANNEL_LINK = "@serafimcloud"

async def main():
    try:
        # Initialize Telegram service
        async with TelegramService() as telegram:
            # Fetch messages from channel
            logger.info("Fetching messages from channel: %s", CHANNEL_LINK)
            messages = await telegram.get_channel_messages(CHANNEL_LINK)
            logger.info("Found %d messages", len(messages))
            
            if not messages:
                logger.warning("No messages found in channel")
                return
            
            # Process messages in batches
            batch_size = 100
            total_vectors = 0
            
            for i in range(0, len(messages), batch_size):
                batch = messages[i:i + batch_size]
                
                # Generate embeddings for batch
                vectors = []
                metadata = []
                ids = []
                
                for msg in batch:
                    # Skip empty messages
                    if not msg["text"].strip():
                        continue
                    
                    # Generate embedding
                    embedding = await generate_embedding(msg["text"])
                    if not embedding:
                        continue
                    
                    vectors.append(embedding)
                    metadata.append({
                        "agent_id": AGENT_ID,
                        "source_link": msg["link"],
                        "text": msg["text"],  # Include the text for better context
                        "date": msg["date"],
                        "views": msg["views"],
                        "forwards": msg["forwards"]
                    })
                    ids.append(str(uuid4()))
                
                if vectors:
                    # Upsert vectors to Pinecone
                    success = await upsert_vectors(vectors, metadata, ids)
                    if success:
                        total_vectors += len(vectors)
                        logger.info(
                            "Processed batch of %d messages (total vectors: %d)",
                            len(vectors), total_vectors
                        )
            
            logger.info("Successfully re-ingested %d vectors", total_vectors)
            
    except Exception as e:
        logger.error("Failed to re-ingest content: %s", str(e))
        logger.error("Error type: %s", type(e).__name__)
        logger.error("Error details:", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main()) 