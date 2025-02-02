"""
Script to reset Pinecone index with correct dimensions.
"""
import os
import logging
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Constants
INDEX_NAME = "agentique"
DIMENSION = 1536  # OpenAI ada-002 embedding dimension
# Convert us-east-1 to us-east-1-aws if needed
PINECONE_ENV = os.getenv("PINECONE_ENV")
if PINECONE_ENV == "us-east-1":
    PINECONE_ENV = "us-east-1-aws"
logger.info("Using Pinecone environment: %s", PINECONE_ENV)

def main():
    try:
        # Delete existing index if it exists
        if INDEX_NAME in pc.list_indexes():
            logger.info("Deleting existing index: %s", INDEX_NAME)
            pc.delete_index(INDEX_NAME)
            logger.info("Successfully deleted index")
        
        # Create new index with correct dimensions
        logger.info("Creating new index with dimension=%d in environment %s", DIMENSION, PINECONE_ENV)
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        logger.info("Successfully created new index")
        
    except Exception as e:
        logger.error("Failed to reset Pinecone index: %s", str(e))
        raise

if __name__ == "__main__":
    main() 