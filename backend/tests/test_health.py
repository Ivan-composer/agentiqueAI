"""
Test script for the health endpoint.
"""
import requests

def test_health():
    """
    Test the /health endpoint to ensure the server is running properly.
    """
    # Ensure server is running on localhost:8000
    url = "http://127.0.0.1:8000/health"
    resp = requests.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok" 