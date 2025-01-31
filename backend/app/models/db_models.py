"""
Pydantic models for database entities.
These models provide type safety and validation for our database operations.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

class UserBase(BaseModel):
    """Base model for User data."""
    telegram_id: str
    username: Optional[str] = None
    credits_balance: int = 0

class UserCreate(UserBase):
    """Model for creating a new user."""
    pass

class User(UserBase):
    """Model for a complete user record."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AgentBase(BaseModel):
    """Base model for Agent data."""
    expert_name: str
    prompt_template: str
    status: str = "active"

class AgentCreate(AgentBase):
    """Model for creating a new agent."""
    owner_id: UUID

class Agent(AgentBase):
    """Model for a complete agent record."""
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatMessageBase(BaseModel):
    """Base model for chat message data."""
    role: str
    content: str

class ChatMessageCreate(ChatMessageBase):
    """Model for creating a new chat message."""
    agent_id: UUID
    user_id: UUID

class ChatMessage(ChatMessageBase):
    """Model for a complete chat message record."""
    id: UUID
    agent_id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    """Base model for transaction data."""
    credits_change: int
    reason: str

class TransactionCreate(TransactionBase):
    """Model for creating a new transaction."""
    user_id: UUID

class Transaction(TransactionBase):
    """Model for a complete transaction record."""
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True 