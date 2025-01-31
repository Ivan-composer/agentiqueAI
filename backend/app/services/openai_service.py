"""
OpenAI service for embeddings and completions.
"""
import os
from typing import List, Dict, Any
from openai import OpenAI, APIError, RateLimitError
from app.utils.logger import logger
from app.utils.errors import ServiceUnavailableError

# Initialize OpenAI client
logger.info("Initializing OpenAI client")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_embedding(text: str) -> List[float]:
    """
    Generate embeddings for a given text using OpenAI's text-embedding-ada-002 model.
    
    Args:
        text: The text to generate embeddings for
    
    Returns:
        List of floats representing the embedding vector
        
    Raises:
        ServiceUnavailableError: If OpenAI service is unavailable
    """
    try:
        logger.debug("Generating embedding for text: %s...", text[:100])
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        logger.info("Successfully generated embedding")
        return response.data[0].embedding
    except (APIError, RateLimitError) as e:
        logger.error("OpenAI service error: %s", str(e))
        raise ServiceUnavailableError("OpenAI", {"error": str(e)})
    except Exception as e:
        logger.error("Failed to generate embedding: %s", str(e))
        raise ServiceUnavailableError("OpenAI", {"error": "Unknown error occurred"})

async def generate_completion(messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 500) -> str:
    """
    Generate a chat completion using OpenAI's GPT model.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum number of tokens to generate
    
    Returns:
        Generated text response
        
    Raises:
        ServiceUnavailableError: If OpenAI service is unavailable
    """
    try:
        logger.debug("Generating completion with %d messages", len(messages))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        logger.info("Successfully generated completion")
        return response.choices[0].message.content
    except (APIError, RateLimitError) as e:
        logger.error("OpenAI service error: %s", str(e))
        raise ServiceUnavailableError("OpenAI", {"error": str(e)})
    except Exception as e:
        logger.error("Failed to generate completion: %s", str(e))
        raise ServiceUnavailableError("OpenAI", {"error": "Unknown error occurred"})

async def moderate_content(text: str) -> Dict[str, Any]:
    """
    Check if text content is appropriate using OpenAI's moderation endpoint.
    
    Args:
        text: The text to moderate
    
    Returns:
        Dictionary containing moderation results
        
    Raises:
        ServiceUnavailableError: If OpenAI service is unavailable
    """
    try:
        logger.debug("Moderating content: %s...", text[:100])
        response = client.moderations.create(input=text)
        result = response.results[0]
        if result.flagged:
            logger.warning("Content was flagged by moderation: %s", result.categories)
        else:
            logger.info("Content passed moderation check")
        return {
            "flagged": result.flagged,
            "categories": result.categories,
            "category_scores": result.category_scores
        }
    except (APIError, RateLimitError) as e:
        logger.error("OpenAI service error: %s", str(e))
        raise ServiceUnavailableError("OpenAI", {"error": str(e)})
    except Exception as e:
        logger.error("Failed to moderate content: %s", str(e))
        raise ServiceUnavailableError("OpenAI", {"error": "Unknown error occurred"}) 