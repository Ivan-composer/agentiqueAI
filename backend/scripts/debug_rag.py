"""
Script to debug RAG retrieval process.
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(backend_dir)

# Verify environment variables
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
os.environ["OPENAI_API_KEY"] = openai_key

from app.services.openai_service import generate_embedding
from app.services.pinecone_service import query_similar
from app.utils.logger import logger

async def debug_rag_retrieval(query: str, agent_id: str = None):
    """Debug the RAG retrieval process."""
    print(f"\nDebug RAG for query: {query}")
    print(f"Agent ID: {agent_id}")
    
    # Generate query embedding
    print("\nGenerating embedding...")
    query_embedding = await generate_embedding(query)
    if not query_embedding:
        print("Failed to generate embedding!")
        return
    
    # Query Pinecone
    print("\nQuerying Pinecone...")
    filter_params = {"agent_id": agent_id} if agent_id else {}
    chunks = await query_similar(
        query_embedding,
        top_k=10,  # Increased from 5
        filter_params=filter_params
    )
    
    if not chunks:
        print("No chunks found!")
        return
        
    print(f"\nFound {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\nChunk {i}:")
        print(f"Text: {chunk['text']}")
        print(f"Score: {chunk.get('score', 0.0):.3f}")
        print(f"Metadata: {chunk['metadata']}")

async def main():
    # Test query
    query = "What was Durov's last post about?"
    agent_id = None  # Replace with actual Durov agent ID
    
    await debug_rag_retrieval(query, agent_id)

if __name__ == "__main__":
    asyncio.run(main()) 