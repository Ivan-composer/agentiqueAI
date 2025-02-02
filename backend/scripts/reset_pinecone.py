"""
Script to reset the Pinecone index.
"""
import os
import sys
import time
import logging
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get environment variables
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
if PINECONE_ENVIRONMENT == "us-east-1":
    PINECONE_ENVIRONMENT = "us-east-1-aws"
logger.info("Using Pinecone environment: %s", PINECONE_ENVIRONMENT)

# Initialize Pinecone
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=PINECONE_ENVIRONMENT
)

# Constants
INDEX_NAME = "agentique-index"
DIMENSION = 1536  # OpenAI ada-002 embedding dimension

def main():
    try:
        # List all indexes
        index_list = pc.list_indexes()
        logger.info("Current indexes: %s", index_list)
        
        # Get list of index names
        index_names = [index['name'] for index in index_list.get('indexes', [])]
        logger.info("Current index names: %s", index_names)
        
        # Delete index if it exists
        if INDEX_NAME in index_names:
            logger.info("Deleting existing index: %s", INDEX_NAME)
            pc.delete_index(INDEX_NAME)
            logger.info("Successfully deleted index: %s", INDEX_NAME)
            logger.info("Waiting for index deletion to complete...")
            time.sleep(30)  # Wait for 30 seconds
        
        # Create new index with correct dimensions
        logger.info("Creating new index with dimension=%d in environment %s", DIMENSION, PINECONE_ENVIRONMENT)
        try:
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
            logger.info("Waiting for index to be ready...")
            time.sleep(30)  # Wait for 30 seconds
            logger.info("Index is ready for use")
        except Exception as create_error:
            if "ALREADY_EXISTS" in str(create_error):
                logger.info("Index already exists, skipping creation")
            else:
                raise
        
    except Exception as e:
        logger.error("Failed to reset index: %s", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main() 