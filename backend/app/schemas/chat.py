from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any


class ChatMessageBase(BaseModel):
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageResponse(ChatMessageBase):
    id: UUID
    project_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class GenerateRequest(BaseModel):
    prompt: str
    stream: bool = True


class EnhancePromptRequest(BaseModel):
    prompt: str


class EnhancePromptResponse(BaseModel):
    original: str
    enhanced: str
    token_count: Dict[str, int]
