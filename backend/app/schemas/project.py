from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class ProjectBase(BaseModel):
    name: str
    framework: str
    project_prompt: Optional[str] = None
    visibility: str = "private"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    framework: Optional[str] = None
    project_prompt: Optional[str] = None
    visibility: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: UUID
    user_id: UUID
    deployment_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
