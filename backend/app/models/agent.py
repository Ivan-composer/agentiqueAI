from typing import Optional
from pydantic import BaseModel

class Agent(BaseModel):
    """Agent model representing a Telegram channel agent"""
    id: str
    user_id: str
    name: str
    channel_link: str
    status: str = "created"  # created, ingesting, ready, failed
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True 