"""
Test error handling functionality across services.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.utils.errors import (
    ServiceError,
    ServiceUnavailableError,
    InsufficientCreditsError,
    TelegramError,
    handle_service_error
)
from app.services.openai_service import generate_embedding, generate_completion, moderate_content
from app.services.pinecone_service import upsert_vectors, query_similar, delete_vectors
from app.services.payment_service import deduct_credits, add_credits
from app.services.telegram_service import TelegramService

class MockResponse:
    """Mock Supabase response object."""
    def __init__(self, data):
        self.data = data

@pytest.mark.asyncio
async def test_openai_service_errors():
    """Test OpenAI service error handling."""
    # Test API error
    with patch('app.services.openai_service.client.embeddings.create', side_effect=Exception("API error")):
        with pytest.raises(ServiceUnavailableError) as exc_info:
            await generate_embedding("test text")
        assert exc_info.value.status_code == 503
        assert "OpenAI service is currently unavailable" in str(exc_info.value)

    # Test rate limit error
    with patch('app.services.openai_service.client.chat.completions.create', side_effect=Exception("Rate limit")):
        with pytest.raises(ServiceUnavailableError) as exc_info:
            await generate_completion([{"role": "user", "content": "test"}])
        assert exc_info.value.status_code == 503

@pytest.mark.asyncio
async def test_pinecone_service_errors():
    """Test Pinecone service error handling."""
    # Test upsert error
    with patch('app.services.pinecone_service.index.upsert', side_effect=Exception("Connection error")):
        with pytest.raises(ServiceUnavailableError) as exc_info:
            await upsert_vectors([], [], [])
        assert exc_info.value.status_code == 503
        assert "Pinecone service is currently unavailable" in str(exc_info.value)

    # Test query error
    with patch('app.services.pinecone_service.index.query', side_effect=Exception("Query failed")):
        with pytest.raises(ServiceUnavailableError) as exc_info:
            await query_similar([0.1] * 1536)
        assert exc_info.value.status_code == 503

@pytest.mark.asyncio
async def test_payment_service_errors():
    """Test payment service error handling."""
    # Test insufficient credits
    mock_response = MockResponse({"credits_balance": 5})
    with patch('app.services.payment_service.supabase.table') as mock_table:
        mock_table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = mock_response
        
        with pytest.raises(InsufficientCreditsError) as exc_info:
            await deduct_credits("user123", 10, "test")
        
        assert exc_info.value.status_code == 403
        assert exc_info.value.details["current_balance"] == 5
        assert exc_info.value.details["required_amount"] == 10

@pytest.mark.asyncio
async def test_telegram_service_errors():
    """Test Telegram service error handling."""
    # Test missing credentials
    with patch.dict('os.environ', {'TELEGRAM_API_ID': '0', 'TELEGRAM_API_HASH': '', 'TELEGRAM_PHONE': ''}):
        with pytest.raises(TelegramError) as exc_info:
            TelegramService()
        assert exc_info.value.status_code == 500
        assert "initialization" in str(exc_info.value)

    # Test connection error
    with patch.dict('os.environ', {
        'TELEGRAM_API_ID': '12345',
        'TELEGRAM_API_HASH': 'test_hash',
        'TELEGRAM_PHONE': '+1234567890'
    }):
        service = TelegramService()
        with patch.object(service.client, 'connect', side_effect=Exception("Connection failed")):
            with pytest.raises(TelegramError) as exc_info:
                await service.connect()
            assert exc_info.value.status_code == 500
            assert "connection" in str(exc_info.value)

def test_handle_service_error():
    """Test service error to HTTP exception conversion."""
    error = ServiceError("Test error", status_code=400, details={"test": "value"})
    http_exc = handle_service_error(error)
    
    assert http_exc.status_code == 400
    assert http_exc.detail["message"] == "Test error"
    assert http_exc.detail["details"] == {"test": "value"} 