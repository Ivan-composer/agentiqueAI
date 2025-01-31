"""
Test credit operations and admin top-ups.
"""
import os
import pytest
from httpx import AsyncClient
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_credit_operations(client: AsyncClient, test_user: str):
    """Test basic credit operations."""
    async for http_client in client:
        async for user_id in test_user:
            # Test adding credits
            response = await http_client.post(f"/credits/add/{user_id}", json={"amount": 100})
            assert response.status_code == 200
            assert response.json()["credits_balance"] == 100
            
            # Test deducting credits
            response = await http_client.post(f"/credits/deduct/{user_id}", json={"amount": 30})
            assert response.status_code == 200
            assert response.json()["credits_balance"] == 70
            
            # Test deducting more credits than available
            response = await http_client.post(f"/credits/deduct/{user_id}", json={"amount": 100})
            assert response.status_code == 400

@pytest.mark.asyncio
async def test_admin_topup(client: AsyncClient, test_user: str):
    """Test admin top-up endpoint."""
    async for http_client in client:
        async for user_id in test_user:
            # Test admin top-up without admin key
            response = await http_client.post(f"/admin/credits/topup/{user_id}", json={"amount": 500})
            assert response.status_code == 403
            
            # Test admin top-up with invalid key
            response = await http_client.post(
                f"/admin/credits/topup/{user_id}", 
                json={"amount": 500},
                headers={"X-Admin-Key": "invalid_key"}
            )
            assert response.status_code == 403
            
            # Test admin top-up with valid key
            response = await http_client.post(
                f"/admin/credits/topup/{user_id}", 
                json={"amount": 500},
                headers={"X-Admin-Key": os.getenv("ADMIN_KEY", "test_admin_key")}
            )
            assert response.status_code == 200
            assert response.json()["credits_balance"] == 500 