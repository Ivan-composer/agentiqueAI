from fastapi import APIRouter

router = APIRouter()

@router.post("/{agent_id}")
async def create_comment(agent_id: str, post_text: str):
    """Create a comment using an agent"""
    return {"comment": "Comment placeholder"}

@router.get("/history")
async def comment_history():
    """Get user's comment history"""
    return {"history": []} 