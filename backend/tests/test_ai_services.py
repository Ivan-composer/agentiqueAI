"""
Tests for AI services (OpenAI and Pinecone).
"""
import pytest
from uuid import uuid4
from app.services.openai_service import generate_embedding, generate_completion, moderate_content
from app.services.pinecone_service import upsert_vectors, query_similar, delete_vectors

async def cleanup_test_vectors():
    """Clean up test vectors from Pinecone."""
    # Delete all test vectors (we'll identify them by metadata)
    results = await query_similar([0.1] * 1536, filter={"source": "test"}, top_k=100)
    if results:
        await delete_vectors([r["id"] for r in results])

@pytest.fixture(autouse=True)
async def setup_and_cleanup():
    """Setup and cleanup before and after each test."""
    await cleanup_test_vectors()
    yield
    await cleanup_test_vectors()

@pytest.mark.asyncio
async def test_openai_embedding():
    """Test OpenAI embedding generation."""
    text = "This is a test text for embedding generation."
    embedding = await generate_embedding(text)
    assert len(embedding) == 1536  # text-embedding-ada-002 dimension
    assert all(isinstance(x, float) for x in embedding)

@pytest.mark.asyncio
async def test_openai_completion():
    """Test OpenAI chat completion."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello!"}
    ]
    response = await generate_completion(messages)
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_openai_moderation():
    """Test OpenAI content moderation."""
    # Test safe content
    safe_text = "Hello, how are you today?"
    safe_result = await moderate_content(safe_text)
    assert not safe_result["flagged"]
    
    # Test unsafe content
    unsafe_text = "I want to harm someone."
    unsafe_result = await moderate_content(unsafe_text)
    assert unsafe_result["flagged"]

@pytest.mark.asyncio
async def test_pinecone_operations():
    """Test Pinecone vector operations."""
    # Test data
    test_id = str(uuid4())
    test_vector = [0.1] * 1536
    test_metadata = {"agent_id": str(uuid4()), "source": "test"}
    
    # Test upsert
    success = await upsert_vectors(
        vectors=[test_vector],
        metadata=[test_metadata],
        ids=[test_id]
    )
    assert success
    
    # Test query with filter
    results = await query_similar(
        test_vector,
        filter={"source": "test"},
        top_k=1
    )
    assert len(results) > 0
    assert results[0]["metadata"]["source"] == "test"
    assert results[0]["score"] > 0.9  # High similarity score expected
    
    # Test delete
    success = await delete_vectors([test_id])
    assert success 