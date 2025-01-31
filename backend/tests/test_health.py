"""
Test the health check endpoint functionality.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException
from app.main import health_check

@pytest.mark.asyncio
async def test_health_check_all_healthy():
    """Test health check when all services are healthy."""
    with patch('app.services.openai_service.client.models.list', new_callable=AsyncMock) as mock_openai, \
         patch('app.services.pinecone_service.pc.list_indexes') as mock_pinecone, \
         patch('app.services.db_service.supabase.table') as mock_supabase:
        
        # Mock successful responses
        mock_openai.return_value = ["model1", "model2"]
        mock_pinecone.return_value = ["index1", "index2"]
        mock_supabase.return_value.select.return_value.limit.return_value.execute.return_value = {"data": []}
        
        # Call health check
        response = await health_check()
        
        # Verify response
        assert response["status"] == "healthy"
        assert response["services"]["openai"] == "healthy"
        assert response["services"]["pinecone"] == "healthy"
        assert response["services"]["supabase"] == "healthy"

@pytest.mark.asyncio
async def test_health_check_openai_unhealthy():
    """Test health check when OpenAI is unhealthy."""
    with patch('app.services.openai_service.client.models.list', new_callable=AsyncMock) as mock_openai, \
         patch('app.services.pinecone_service.pc.list_indexes') as mock_pinecone, \
         patch('app.services.db_service.supabase.table') as mock_supabase:
        
        # Mock responses
        mock_openai.side_effect = Exception("API error")
        mock_pinecone.return_value = ["index1", "index2"]
        mock_supabase.return_value.select.return_value.limit.return_value.execute.return_value = {"data": []}
        
        # Call health check and expect exception
        with pytest.raises(HTTPException) as exc_info:
            await health_check()
        
        # Verify response
        assert exc_info.value.status_code == 503
        assert exc_info.value.detail["status"] == "unhealthy"
        assert exc_info.value.detail["services"]["openai"] == "unhealthy"
        assert exc_info.value.detail["services"]["pinecone"] == "healthy"
        assert exc_info.value.detail["services"]["supabase"] == "healthy"

@pytest.mark.asyncio
async def test_health_check_all_unhealthy():
    """Test health check when all services are unhealthy."""
    with patch('app.services.openai_service.client.models.list', new_callable=AsyncMock) as mock_openai, \
         patch('app.services.pinecone_service.pc.list_indexes') as mock_pinecone, \
         patch('app.services.db_service.supabase.table') as mock_supabase:
        
        # Mock failed responses
        mock_openai.side_effect = Exception("API error")
        mock_pinecone.side_effect = Exception("Connection error")
        mock_supabase.side_effect = Exception("DB error")
        
        # Call health check and expect exception
        with pytest.raises(HTTPException) as exc_info:
            await health_check()
        
        # Verify response
        assert exc_info.value.status_code == 503
        assert exc_info.value.detail["status"] == "unhealthy"
        assert exc_info.value.detail["services"]["openai"] == "unhealthy"
        assert exc_info.value.detail["services"]["pinecone"] == "unhealthy"
        assert exc_info.value.detail["services"]["supabase"] == "unhealthy" 