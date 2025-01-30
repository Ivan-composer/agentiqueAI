import os
from typing import List, Dict, Any, Optional, Union
from dotenv import load_dotenv
import requests
import json
from langchain.llms.base import LLM
from langchain.embeddings.base import Embeddings
from langchain.prompts import PromptTemplate
import logging
from datetime import datetime
import numpy as np
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("Missing required OpenRouter API key")
if not HUGGINGFACE_API_KEY:
    raise ValueError("Missing required HuggingFace API key")

# Define headers for OpenRouter API
OPENROUTER_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://agentique.ai",
    "X-Title": "Agentique AI"
}

# Define headers for Hugging Face API
HUGGINGFACE_HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

# Define the default agent prompt template
DEFAULT_AGENT_TEMPLATE = """You are {agent_name}, an AI agent with access to content from a specific Telegram channel.
Your role is to assist users by providing information and insights based solely on the content available in your knowledge base.

Context from the channel:
{context}

User Question: {question}

Instructions:
1. Answer based ONLY on the provided context
2. If you can't answer from the context, say so
3. Include relevant source references as a numbered list at the end
4. Keep your tone professional but conversational
5. Be concise but informative

Your response:"""

AGENT_PROMPT = PromptTemplate(
    input_variables=["agent_name", "context", "question"],
    template=DEFAULT_AGENT_TEMPLATE
)

class HuggingFaceEmbeddings(Embeddings):
    """LangChain Embeddings class for Hugging Face's API"""
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple documents"""
        try:
            print(f"\n[HuggingFaceEmbeddings] Starting embedding generation")
            print(f"[HuggingFaceEmbeddings] Number of texts: {len(texts)}")
            print(f"[HuggingFaceEmbeddings] First text preview: {texts[0][:100]}...")
            
            # Using all-MiniLM-L6-v2 which outputs 384-dimensional embeddings
            response = requests.post(
                url="https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2",
                headers=HUGGINGFACE_HEADERS,
                json={"inputs": texts, "options": {"wait_for_model": True}}
            )
            print(f"[HuggingFaceEmbeddings] Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[HuggingFaceEmbeddings] Error response: {response.text}")
                raise Exception(f"HuggingFace API returned status {response.status_code}")
                
            embeddings = response.json()
            print(f"[HuggingFaceEmbeddings] Successfully generated {len(embeddings)} embeddings")
            print(f"[HuggingFaceEmbeddings] First embedding dimension: {len(embeddings[0])}")
            
            return embeddings
            
        except Exception as e:
            print(f"\n[HuggingFaceEmbeddings] Error generating embeddings:")
            print(f"[HuggingFaceEmbeddings] Error type: {type(e).__name__}")
            print(f"[HuggingFaceEmbeddings] Error message: {str(e)}")
            if isinstance(e, requests.exceptions.RequestException):
                print(f"[HuggingFaceEmbeddings] Response status: {e.response.status_code if e.response else 'No response'}")
                print(f"[HuggingFaceEmbeddings] Response body: {e.response.text if e.response else 'No response body'}")
            print("\nTraceback:")
            import traceback
            traceback.print_exc()
            raise
    
    def embed_query(self, text: str) -> List[float]:
        """Get embeddings for a single query"""
        return self.embed_documents([text])[0]

class OpenRouterGeminiLLM(LLM):
    """Custom LangChain LLM class for OpenRouter's Gemini"""
    
    @property
    def _llm_type(self) -> str:
        return "openrouter-gemini"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Call the OpenRouter API using Gemini model"""
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=OPENROUTER_HEADERS,
                json={
                    "model": "google/gemini-2.0-flash-thinking-exp:free",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling OpenRouter Gemini API: {str(e)}")
            raise

# Update instances
openrouter_gemini_llm = OpenRouterGeminiLLM()
huggingface_embeddings = HuggingFaceEmbeddings()

# Set the current active LLM and embeddings
current_llm = openrouter_gemini_llm
current_embeddings = huggingface_embeddings

# Initialize global instances
llm = current_llm
embeddings = current_embeddings

async def generate_response(prompt: str, stop: Optional[List[str]] = None) -> str:
    """Generate a response using the current LLM"""
    try:
        return llm._call(prompt, stop)
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I apologize, but I encountered an error. Please try again."

async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Get embeddings for a list of texts using HuggingFace API"""
    try:
        print(f"\n[LLMService] Getting embeddings for {len(texts)} texts")
        return current_embeddings.embed_documents(texts)
    except Exception as e:
        print(f"Error getting embeddings: {str(e)}")
        return []

async def get_query_embedding(text: str) -> List[float]:
    """Get embedding for a single query text"""
    try:
        print(f"\n[LLMService] Getting embedding for query: {text[:100]}...")
        return current_embeddings.embed_query(text)
    except Exception as e:
        print(f"Error getting query embedding: {str(e)}")
        return []

class LLMService:
    def __init__(self):
        """Initialize LLM service"""
        # TODO: Initialize LLM client when we implement actual LLM integration
        pass

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for a list of texts
        For now, return dummy embeddings of the correct dimension
        """
        # TODO: Implement actual embedding logic
        # For now, return dummy embeddings of dimension 384 (matching our Pinecone index)
        return [[0.0] * 384 for _ in texts]

    async def get_completion(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Get completion from the LLM
        For now, return a placeholder response
        """
        # TODO: Implement actual LLM completion logic
        return "This is a placeholder response. The actual LLM integration will be implemented later."

# Create a singleton instance
llm_service = LLMService()

# Export functions
__all__ = [
    'get_embeddings',
    'get_query_embedding',
    'get_completion',
    'llm_service'
] 