"""
Pinecone service for vector similarity search.
"""
import os
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from uuid import UUID
from app.utils.logger import logger

# Initialize Pinecone
logger.info("Initializing Pinecone client")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create index if it doesn't exist
INDEX_NAME = "agentique-index"
DIMENSION = 1536  # OpenAI's text-embedding-ada-002 dimension

if INDEX_NAME not in pc.list_indexes().names():
    logger.info("Creating new Pinecone index: %s", INDEX_NAME)
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=os.getenv("PINECONE_ENV", "us-west-2")
        )
    )
else:
    logger.info("Using existing Pinecone index: %s", INDEX_NAME)

# Get index instance
index = pc.Index(INDEX_NAME)

async def upsert_vectors(vectors: List[List[float]], metadata: List[Dict[str, Any]], ids: List[str]) -> bool:
    """
    Upsert vectors to Pinecone.
    
    Args:
        vectors: List of embedding vectors
        metadata: List of metadata dicts for each vector
        ids: List of unique IDs for each vector
    
    Returns:
        bool: True if successful
    """
    try:
        logger.debug("Upserting %d vectors to Pinecone", len(vectors))
        # Prepare vector data
        vectors_data = list(zip(ids, vectors, metadata))
        
        # Upsert to Pinecone
        index.upsert(vectors=vectors_data)
        logger.info("Successfully upserted %d vectors", len(vectors))
        return True
    except Exception as e:
        logger.error("Error upserting vectors: %s", str(e))
        return False

async def query_similar(
    query_vector: List[float],
    top_k: int = 5,
    agent_id: Optional[UUID] = None,
    filter: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Query similar vectors from Pinecone.
    
    Args:
        query_vector: The query embedding vector
        top_k: Number of results to return
        agent_id: Optional agent ID to filter results
        filter: Optional filter dictionary to apply to the query
    
    Returns:
        List of similar items with their metadata
    """
    try:
        # Prepare filter
        filter_dict = filter or {}
        if agent_id:
            filter_dict["agent_id"] = str(agent_id)
        
        logger.debug("Querying Pinecone with top_k=%d and filter=%s", top_k, filter_dict)
        
        # Query Pinecone
        results = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict if filter_dict else None
        )
        
        # Format results
        formatted_results = [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            }
            for match in results.matches
        ]
        
        logger.info("Found %d similar vectors", len(formatted_results))
        return formatted_results
    except Exception as e:
        logger.error("Error querying vectors: %s", str(e))
        return []

async def delete_vectors(ids: List[str]) -> bool:
    """
    Delete vectors from Pinecone.
    
    Args:
        ids: List of vector IDs to delete
    
    Returns:
        bool: True if successful
    """
    try:
        logger.debug("Deleting %d vectors from Pinecone", len(ids))
        index.delete(ids=ids)
        logger.info("Successfully deleted %d vectors", len(ids))
        return True
    except Exception as e:
        logger.error("Error deleting vectors: %s", str(e))
        return False 