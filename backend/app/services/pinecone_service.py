"""
Pinecone service for vector similarity search.
"""
import os
from typing import List, Dict, Any
from pinecone import Pinecone, PodSpec
from app.utils.logger import logger

# Initialize Pinecone client
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")  # Use standardized environment
)

# Get or create index
INDEX_NAME = "agentique"
DIMENSION = 1536  # OpenAI ada-002 embedding dimension

try:
    # Get index if it exists
    index = pc.Index(INDEX_NAME)
    logger.info("Connected to existing Pinecone index: %s", INDEX_NAME)
except Exception as e:
    # Create index if it doesn't exist
    logger.info("Creating new Pinecone index with environment: %s", os.getenv("PINECONE_ENVIRONMENT"))
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=PodSpec(environment=os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws"))
    )
    index = pc.Index(INDEX_NAME)
    logger.info("Created new Pinecone index: %s", INDEX_NAME)

async def query_similar(
    query_vector: List[float],
    top_k: int = 5,
    filter_params: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """
    Query Pinecone for similar vectors.
    
    Args:
        query_vector: The query embedding
        top_k: Number of results to return
        filter_params: Optional filter parameters
        
    Returns:
        List of similar chunks with metadata
    """
    try:
        # Query the index
        results = index.query(
            vector=query_vector,
            top_k=top_k,
            filter=filter_params,
            include_metadata=True
        )
        
        # Format results
        chunks = []
        for match in results.matches:
            if match.metadata:
                chunks.append({
                    'text': match.metadata.get('text', ''),
                    'metadata': match.metadata,
                    'score': match.score
                })
        
        return chunks
        
    except Exception as e:
        logger.error("Failed to query Pinecone: %s", str(e))
        return []

async def upsert_vectors(
    vectors: List[List[float]],
    metadata: List[Dict[str, Any]],
    ids: List[str]
) -> bool:
    """
    Upsert vectors to Pinecone.
    
    Args:
        vectors: List of vector embeddings
        metadata: List of metadata dictionaries
        ids: List of unique IDs
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Prepare records
        records = [
            {
                'id': id_,
                'values': vector,
                'metadata': meta
            }
            for id_, vector, meta in zip(ids, vectors, metadata)
        ]
        
        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            index.upsert(vectors=batch)
            
        return True
        
    except Exception as e:
        logger.error("Failed to upsert vectors: %s", str(e))
        return False

async def delete_vectors(ids: List[str]) -> bool:
    """
    Delete vectors from Pinecone.
    
    Args:
        ids: List of vector IDs to delete
    
    Returns:
        bool: True if successful
        
    Raises:
        ServiceUnavailableError: If Pinecone service is unavailable
    """
    try:
        logger.debug("Deleting %d vectors from Pinecone", len(ids))
        index.delete(ids=ids)
        logger.info("Successfully deleted %d vectors", len(ids))
        return True
    except Exception as e:
        logger.error("Error deleting vectors: %s", str(e))
        return False 