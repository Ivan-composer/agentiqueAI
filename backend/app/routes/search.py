"""
Search-related routes for finding agents and content.
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.db_models import Agent

router = APIRouter()

@router.get("/agents", response_model=List[Agent])
async def search_agents(query: str = ""):
    """Search for agents by name or description."""
    # TODO: Implement agent search with vector similarity
    return [] 