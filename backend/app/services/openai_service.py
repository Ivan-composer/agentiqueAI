"""
OpenAI service for generating embeddings and completions.
"""
import os
from typing import Optional, List, Dict, Any
from openai import AsyncOpenAI, APIError, RateLimitError
from app.utils.logger import logger
from app.utils.errors import ServiceUnavailableError

# Initialize OpenAI client
logger.info("Initializing OpenAI client")
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_embedding(text: str) -> Optional[List[float]]:
    """
    Generate an embedding for the given text using OpenAI's API.
    
    Args:
        text: The text to generate an embedding for
        
    Returns:
        List of floats representing the embedding, or None if failed
    """
    try:
        logger.debug("Generating embedding for text: %s...", text[:100])
        response = await client.embeddings.create(
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
        return None

async def generate_completion(prompt: str) -> str:
    """
    Generate a completion for the given prompt using OpenAI's API.
    
    Args:
        prompt: The prompt to generate a completion for
        
    Returns:
        The generated completion text
    """
    try:
        logger.debug("Generating completion with prompt: %s...", prompt[:100])
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        logger.info("Successfully generated completion")
        return response.choices[0].message.content
    except (APIError, RateLimitError) as e:
        logger.error("OpenAI service error: %s", str(e))
        raise ServiceUnavailableError("OpenAI", {"error": str(e)})
    except Exception as e:
        logger.error("Failed to generate completion: %s", str(e))
        return "I encountered an error while generating a response. Please try again."

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
        response = await client.moderations.create(input=text)
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