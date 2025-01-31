"""
Test the unified RAG service functionality.
"""
import pytest
from unittest.mock import patch
from app.services.rag_service import rag_retrieve_and_summarize

@pytest.mark.asyncio
async def test_rag_chat_mode():
    """Test RAG in chat mode with agent_id filter."""
    # Mock data
    test_query = "What's the latest update?"
    test_agent_id = "test-agent-123"
    mock_chunks = [
        {
            "id": "1",
            "metadata": {
                "text": "Latest update: New feature released",
                "source_link": "https://t.me/test/1"
            },
            "score": 0.9
        }
    ]
    
    # Mock responses
    mock_embedding = [0.1] * 1536  # OpenAI ada-002 dimension
    mock_completion = "Based on the latest update, a new feature was released."
    
    # Set up mocks
    with patch('app.services.rag_service.generate_embedding', return_value=mock_embedding), \
         patch('app.services.rag_service.query_similar', return_value=mock_chunks), \
         patch('app.services.rag_service.generate_completion', return_value=mock_completion):
        
        # Call function
        result = await rag_retrieve_and_summarize(test_query, agent_id=test_agent_id, mode="chat")
        
        # Verify result
        assert result == mock_completion

@pytest.mark.asyncio
async def test_rag_search_mode():
    """Test RAG in search mode without agent_id filter."""
    # Mock data
    test_query = "Find all updates"
    mock_chunks = [
        {
            "id": "1",
            "metadata": {
                "text": "Update 1: Feature A",
                "source_link": "https://t.me/test/1"
            },
            "score": 0.9
        },
        {
            "id": "2",
            "metadata": {
                "text": "Update 2: Feature B",
                "source_link": "https://t.me/test/2"
            },
            "score": 0.8
        }
    ]
    
    # Mock responses
    mock_embedding = [0.1] * 1536
    mock_completion = "Here are the recent updates: Feature A and Feature B were released."
    
    # Set up mocks
    with patch('app.services.rag_service.generate_embedding', return_value=mock_embedding), \
         patch('app.services.rag_service.query_similar', return_value=mock_chunks), \
         patch('app.services.rag_service.generate_completion', return_value=mock_completion):
        
        # Call function
        result = await rag_retrieve_and_summarize(test_query, mode="search")
        
        # Verify result
        assert result == mock_completion

@pytest.mark.asyncio
async def test_rag_invalid_mode():
    """Test RAG with invalid mode raises ValueError."""
    with pytest.raises(ValueError, match="Invalid mode. Must be 'chat' or 'search'"):
        await rag_retrieve_and_summarize("test query", mode="invalid") 