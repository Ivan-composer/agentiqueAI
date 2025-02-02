"""
Script to check Pinecone index status.
Uses environment variables from .env file:
PINECONE_API_KEY - Your Pinecone API key
PINECONE_ENVIRONMENT - Pinecone environment (us-east-1-aws)
"""
import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables from .env
load_dotenv()

# Initialize Pinecone
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")
)

# Get index
index = pc.Index("agentique")

# Print index stats
print("\nPinecone Configuration:")
print(f"Environment: {os.getenv('PINECONE_ENVIRONMENT', 'us-east-1-aws')}")
print(f"API Key: {os.getenv('PINECONE_API_KEY')[:10]}...")

print("\nIndex Statistics:")
print(index.describe_index_stats()) 