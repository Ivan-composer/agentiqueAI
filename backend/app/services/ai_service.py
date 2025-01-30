"""
AI Service Module for AgentiqueAI.

This module centralizes all AI-related functionality, including interactions with OpenAI and Pinecone.
It provides a clean interface for generating embeddings and performing vector similarity searches.
"""

import os
from typing import List, Dict, Any, Optional
import openai
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIService:
    """
    A service class that handles all AI-related operations.
    
    This class manages interactions with OpenAI for embeddings and Pinecone for vector similarity search.
    It ensures proper initialization of API keys and provides a clean interface for AI operations.
    """
    
    def __init__(self):
        """
        Initialize the AIService with necessary API keys and configurations.
        
        Raises:
            ValueError: If required environment variables are not set.
        """
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.pinecone_api_key = os.environ.get("PINECONE_API_KEY")
        self.pinecone_env = os.environ.get("PINECONE_ENV")
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        if not self.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY environment variable is not set")
            
        # Initialize APIs
        openai.api_key = self.openai_api_key
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.pinecone_api_key)

        # Initialize configuration
        self.index_name = "agentique-index"

        # Create index if it doesn't exist
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=384,  # all-MiniLM-L6-v2 embedding dimension
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"  # Correct AWS region format
                )
            )

        # Initialize Pinecone index
        self.index = self.pc.Index(self.index_name)
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding vector for the given text using OpenAI's API.
        
        Args:
            text (str): The input text to generate an embedding for.
            
        Returns:
            List[float]: The embedding vector as a list of floats.
            
        Raises:
            openai.error.OpenAIError: If there's an error with the OpenAI API call.
        """
        try:
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response['data'][0]['embedding']
        except openai.error.OpenAIError as e:
            # Log the error and re-raise
            print(f"Error generating embedding: {str(e)}")
            raise
    
    def query_pinecone(
        self,
        vector: List[float],
        top_k: int = 5,
        namespace: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Query Pinecone index for similar vectors.
        
        Args:
            vector (List[float]): The query vector to find similarities for.
            top_k (int, optional): Number of results to return. Defaults to 5.
            namespace (str, optional): Pinecone namespace to query. Defaults to None.
            
        Returns:
            List[Dict[str, Any]]: List of similar items with their metadata and scores.
            
        Raises:
            pinecone.exceptions.PineconeException: If there's an error with the Pinecone query.
        """
        try:
            results = self.index.query(
                vector=vector,
                top_k=top_k,
                include_metadata=True,
                namespace=namespace
            )
            return results.matches
        except Exception as e:
            # Log the error and re-raise
            print(f"Error querying Pinecone: {str(e)}")
            raise
    
    def upsert_to_pinecone(
        self,
        vectors: List[tuple],
        namespace: Optional[str] = None
    ) -> bool:
        """
        Upsert vectors to Pinecone index.
        
        Args:
            vectors (List[tuple]): List of (id, vector, metadata) tuples to upsert.
            namespace (str, optional): Pinecone namespace to upsert to. Defaults to None.
            
        Returns:
            bool: True if upsert was successful, False otherwise.
            
        Raises:
            pinecone.exceptions.PineconeException: If there's an error with the Pinecone upsert.
        """
        try:
            self.index.upsert(vectors=vectors, namespace=namespace)
            return True
        except Exception as e:
            # Log the error and re-raise
            print(f"Error upserting to Pinecone: {str(e)}")
            raise
    
    def delete_from_pinecone(
        self,
        ids: List[str],
        namespace: Optional[str] = None
    ) -> bool:
        """
        Delete vectors from Pinecone index.
        
        Args:
            ids (List[str]): List of vector IDs to delete.
            namespace (str, optional): Pinecone namespace to delete from. Defaults to None.
            
        Returns:
            bool: True if deletion was successful, False otherwise.
            
        Raises:
            pinecone.exceptions.PineconeException: If there's an error with the Pinecone deletion.
        """
        try:
            self.index.delete(ids=ids, namespace=namespace)
            return True
        except Exception as e:
            # Log the error and re-raise
            print(f"Error deleting from Pinecone: {str(e)}")
            raise 