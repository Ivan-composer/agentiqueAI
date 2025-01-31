"""
Pytest configuration and fixtures.
"""
import os
import pytest
from dotenv import load_dotenv
import uuid
import asyncio

# Load environment variables from .env file
load_dotenv()

def pytest_configure(config):
    """Configure pytest."""
    # Add id_generator function to pytest namespace
    pytest.id_generator = lambda: str(uuid.uuid4())[:8]

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close() 