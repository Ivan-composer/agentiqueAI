from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import logging

from ..services.db_service import (
    get_user_by_telegram_id,
    create_user,
    create_agent,
    get_user_agents,
    get_agent
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class AgentCreate(BaseModel):
    name: str
    channel_link: str

async def get_current_user() -> str:
    """Get current user ID for testing"""
    # For testing, get the test user
    test_user = await get_user_by_telegram_id("test_user")
    if not test_user:
        test_user = await create_user(
            telegram_id="test_user",
            username="test_user"
        )
    return test_user["id"]  # Return the UUID of the test user

@router.post("/")
async def create_new_agent(
    agent: AgentCreate,
    user_id: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """Create a new agent"""
    try:
        new_agent = await create_agent(
            user_id=user_id,
            name=agent.name,
            channel_link=agent.channel_link
        )
        
        if not new_agent:
            raise HTTPException(status_code=500, detail="Failed to create agent")
            
        return {
            "success": True,
            "agent": new_agent
        }
        
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_agents(
    user_id: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """List all agents for the current user"""
    try:
        agents = await get_user_agents(user_id)
        return {
            "success": True,
            "agents": agents
        }
        
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}")
async def get_agent_by_id(
    agent_id: str,
    user_id: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get a specific agent by ID"""
    try:
        agent = await get_agent(agent_id)
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
            
        # Check if agent belongs to user
        if agent["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this agent")
            
        return {
            "success": True,
            "agent": agent
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 