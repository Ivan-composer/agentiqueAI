import os
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import json
from datetime import datetime
from . import llm_service  # Add this import
import asyncio

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

if not PINECONE_API_KEY or not PINECONE_ENV:
    raise ValueError("Missing required Pinecone environment variables")

# Initialize Pinecone with new client format
pc = Pinecone(api_key=PINECONE_API_KEY)

class VectorService:
    def __init__(self, index_name: str = "agentique"):
        """Initialize VectorService with a Pinecone index"""
        self.index_name = index_name
        self._index = None  # Initialize as None
        
    @property
    def index(self):
        """Lazy initialization of Pinecone index"""
        if self._index is None:
            self._index = pc.Index(self.index_name)
        return self._index

    async def verify_index(self):
        """Verify that the Pinecone index exists and is properly configured"""
        try:
            print(f"\n[VectorService] Verifying index {self.index_name}")
            
            # Check if index exists
            existing_indexes = [index.name for index in pc.list_indexes()]
            print(f"[VectorService] Existing indexes: {existing_indexes}")
            
            needs_creation = True
            
            if self.index_name in existing_indexes:
                # Verify index configuration
                stats = self.index.describe_index_stats()
                print(f"[VectorService] Index stats: {stats}")
                
                # Check dimension
                if 'dimension' in stats and stats['dimension'] != 384:
                    print(f"[VectorService] Index dimension mismatch. Expected 384, got {stats['dimension']}")
                    print(f"[VectorService] Deleting index {self.index_name} to recreate with correct dimension")
                    pc.delete_index(self.index_name)
                else:
                    needs_creation = False
            
            if needs_creation:
                print(f"[VectorService] Creating new index: {self.index_name}")
                pc.create_index(
                    name=self.index_name,
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=PINECONE_ENV
                    ),
                    dimension=384,  # all-MiniLM-L6-v2 embedding dimension
                    metric="cosine"
                )
                print("[VectorService] Successfully created new index")
                self._index = pc.Index(self.index_name)  # Reinitialize after creation
            
            print("[VectorService] Index verification completed successfully")
            
        except Exception as e:
            print(f"\n[VectorService] Error verifying index:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            raise

    async def _upsert_vectors(self, vectors: List[Dict[str, Any]]):
        """Helper method to upsert vectors to Pinecone"""
        try:
            print(f"\n[VectorService] Starting vector upsert")
            print(f"[VectorService] Number of vectors: {len(vectors)}")
            
            if vectors:
                print(f"[VectorService] First vector ID: {vectors[0]['id']}")
                print(f"[VectorService] First vector dimension: {len(vectors[0]['values'])}")
                print(f"[VectorService] First vector metadata: {vectors[0]['metadata']}")
            
            # Convert vectors to the format expected by new Pinecone client
            formatted_vectors = [(vec["id"], vec["values"], vec["metadata"]) for vec in vectors]
            print(f"[VectorService] Formatted {len(formatted_vectors)} vectors for Pinecone")
            print(f"[VectorService] First formatted vector: {formatted_vectors[0] if formatted_vectors else None}")
            
            # Perform upsert with error handling
            try:
                self.index.upsert(vectors=formatted_vectors)
                print(f"[VectorService] Successfully upserted vectors to Pinecone")
            except Exception as upsert_error:
                print(f"[VectorService] Upsert error: {str(upsert_error)}")
                raise
            
            # Verify the upsert with retries
            max_retries = 3
            retry_delay = 1  # seconds
            
            for attempt in range(max_retries):
                try:
                    stats = self.index.describe_index_stats()
                    print(f"[VectorService] Current index stats (attempt {attempt + 1}): {stats}")
                    
                    if stats.total_vector_count > 0:
                        print(f"[VectorService] Vectors confirmed in index")
                        break
                        
                    print(f"[VectorService] No vectors found, retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    
                except Exception as stats_error:
                    print(f"[VectorService] Error getting stats (attempt {attempt + 1}): {str(stats_error)}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                    else:
                        raise
            
        except Exception as e:
            print(f"\n[VectorService] Error in _upsert_vectors:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("\nTraceback:")
            import traceback
            traceback.print_exc()
            raise

    async def delete_agent_vectors(self, agent_id: str) -> bool:
        """Delete all vectors for a specific agent"""
        try:
            print(f"[VectorService] Deleting vectors for agent {agent_id}")
            
            # First, get all vector IDs for this agent
            results = self.index.query(
                vector=[0.0] * 384,  # Dummy vector
                filter={"agent_id": {"$eq": agent_id}},
                top_k=10000,  # Adjust based on expected maximum
                include_values=False
            )
            
            matches = results.matches if hasattr(results, 'matches') else []
            if not matches:
                print(f"[VectorService] No vectors found for agent {agent_id}")
                return True
                
            # Get vector IDs
            vector_ids = [match.id for match in matches]
            print(f"[VectorService] Found {len(vector_ids)} vectors to delete")
            
            # Delete vectors in batches of 1000
            batch_size = 1000
            for i in range(0, len(vector_ids), batch_size):
                batch = vector_ids[i:i + batch_size]
                self.index.delete(ids=batch)
                print(f"[VectorService] Deleted batch of {len(batch)} vectors")
            
            print(f"[VectorService] Successfully deleted all vectors for agent {agent_id}")
            return True
            
        except Exception as e:
            print(f"[VectorService] Error deleting vectors:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("\nTraceback:")
            import traceback
            traceback.print_exc()
            return False

    async def search_vectors(
        self,
        query_vector: List[float],
        agent_id: str = None,
        top_k: int = 5,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        try:
            print(f"\n[VectorService] Starting vector search:")
            print(f"[VectorService] Agent ID: {agent_id}")
            print(f"[VectorService] Query vector dimension: {len(query_vector)}")
            print(f"[VectorService] Top K: {top_k}")
            
            filter_dict = {"agent_id": {"$eq": agent_id}} if agent_id else {}
            print(f"[VectorService] Filter: {filter_dict}")
            
            # Use the correct method for the latest Pinecone client
            print("[VectorService] Executing query...")
            results = self.index.query(
                vector=query_vector,
                filter=filter_dict,
                top_k=top_k,
                include_metadata=True
            )
            
            print(f"[VectorService] Raw results: {results}")
            matches = results.matches if hasattr(results, 'matches') else []
            print(f"[VectorService] Found {len(matches)} matches")
            
            # Filter by score threshold
            matches = [
                match for match in matches
                if match.score >= score_threshold
            ]
            
            if matches:
                print("\n[VectorService] First match details:")
                print(f"Score: {matches[0].score}")
                print(f"Metadata: {matches[0].metadata}")
                print(f"ID: {matches[0].id}")
            
            return matches
            
        except Exception as e:
            print(f"\n[VectorService] Error searching vectors:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("\nTraceback:")
            import traceback
            traceback.print_exc()
            return []

    async def process_and_store(self, messages: List[Dict[str, Any]], agent_id: str) -> bool:
        """
        Process messages and store their vectors
        
        Args:
            messages: List of message dictionaries with 'text' and 'message_id' keys
            agent_id: ID of the agent these messages belong to
        """
        try:
            print(f"\n[VectorService] Starting to process {len(messages)} messages for agent {agent_id}")
            
            vectors = []
            batch_texts = []
            batch_metadata = []
            
            for msg in messages:
                print(f"\n[VectorService] Processing message: {msg.get('message_id', 'unknown')}")
                print(f"[VectorService] Message text: {msg.get('text', '')[:100]}...")  # First 100 chars
                
                # Create metadata for the message
                metadata = {
                    "agent_id": agent_id,
                    "message_id": msg.get("message_id", ""),
                    "timestamp": msg.get("timestamp", datetime.now().isoformat()),
                    "text": msg["text"],
                    "source_link": msg.get("link", "")
                }
                
                batch_texts.append(msg["text"])
                batch_metadata.append(metadata)
                
                if len(batch_texts) >= 10:  # Process in smaller batches for embeddings
                    print(f"\n[VectorService] Processing batch of {len(batch_texts)} texts")
                    # Get embeddings for the batch
                    embeddings = await llm_service.get_embeddings(batch_texts)
                    print(f"[VectorService] Got {len(embeddings)} embeddings")
                    
                    if embeddings:
                        print(f"[VectorService] First embedding dimension: {len(embeddings[0])}")
                    
                    # Create vectors with embeddings
                    for i, (embedding, metadata) in enumerate(zip(embeddings, batch_metadata)):
                        vectors.append({
                            "id": f"{agent_id}_{metadata['message_id']}",
                            "values": embedding,
                            "metadata": metadata
                        })
                    
                    # Reset batches
                    batch_texts = []
                    batch_metadata = []
                
                if len(vectors) >= 100:  # Batch upserts to Pinecone
                    print(f"\n[VectorService] Upserting batch of {len(vectors)} vectors")
                    await self._upsert_vectors(vectors)
                    vectors = []
            
            # Process any remaining texts
            if batch_texts:
                print(f"\n[VectorService] Processing final batch of {len(batch_texts)} texts")
                embeddings = await llm_service.get_embeddings(batch_texts)
                print(f"[VectorService] Got {len(embeddings)} embeddings for final batch")
                
                if embeddings:
                    print(f"[VectorService] First embedding dimension: {len(embeddings[0])}")
                
                for i, (embedding, metadata) in enumerate(zip(embeddings, batch_metadata)):
                    vectors.append({
                        "id": f"{agent_id}_{metadata['message_id']}",
                        "values": embedding,
                        "metadata": metadata
                    })
            
            # Upsert any remaining vectors
            if vectors:
                print(f"\n[VectorService] Upserting final batch of {len(vectors)} vectors")
                await self._upsert_vectors(vectors)
            
            print(f"\n[VectorService] Successfully completed processing and storing vectors")
            return True
            
        except Exception as e:
            print(f"\n[VectorService] Error processing messages:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("\nTraceback:")
            import traceback
            traceback.print_exc()
            return False

    async def count_vectors(self, agent_id: str = None) -> int:
        """Count vectors for an agent"""
        try:
            print(f"\n[VectorService] Counting vectors for agent: {agent_id}")
            
            # Get index stats
            stats = self.index.describe_index_stats()
            print(f"[VectorService] Raw index stats: {stats}")
            
            if not agent_id:
                # Return total vector count
                total_count = stats.total_vector_count if hasattr(stats, 'total_vector_count') else 0
                print(f"[VectorService] Total vector count: {total_count}")
                return total_count
            
            # For agent-specific count, we'll use a fetch operation
            # Create a dummy vector of the correct dimension
            dummy_vector = [0.0] * 384
            
            # Fetch with a high top_k to get all vectors for the agent
            # Note: This might need pagination for very large sets
            results = self.index.query(
                vector=dummy_vector,
                filter={"agent_id": {"$eq": agent_id}},
                top_k=10000,  # Adjust based on expected maximum
                include_values=False
            )
            
            # Count the matches
            matches = results.matches if hasattr(results, 'matches') else []
            count = len(matches)
            
            print(f"[VectorService] Vector count for agent {agent_id}: {count}")
            if count > 0:
                print(f"[VectorService] Sample vector IDs: {[m.id for m in matches[:3]]}")
            
            return count
            
        except Exception as e:
            print(f"\n[VectorService] Error counting vectors:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("\nTraceback:")
            import traceback
            traceback.print_exc()
            return 0

# Create singleton instance
vector_service = VectorService() 