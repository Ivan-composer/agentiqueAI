"""
Script to test if text is being stored in Pinecone metadata.
"""
import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables first
load_dotenv()

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# Now we can import from app
from app.services.pinecone_service import query_similar
from app.services.openai_service import generate_embedding

async def main():
    # Test query
    query = "What was Durov's last post about?"
    logger.info("Query: %s", query)
    
    # Generate embedding for query
    embedding = await generate_embedding(query)
    
    # Get similar documents
    results = await query_similar(embedding)
    
    # Print results
    for i, result in enumerate(results, 1):
        logger.info("\nResult %d:", i)
        logger.info("Score: %f", result['score'])
        logger.info("Text: %s", result['metadata'].get('text', 'No text available'))

if __name__ == "__main__":
    asyncio.run(main()) 