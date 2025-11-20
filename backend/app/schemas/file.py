from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class ProjectFileBase(BaseModel):
    path: str
    content: str
    language: Optional[str] = None
    is_locked: bool = False


class ProjectFileCreate(ProjectFileBase):
    pass


class ProjectFileUpdate(BaseModel):
    content: Optional[str] = None
    is_locked: Optional[bool] = None


class ProjectFileResponse(ProjectFileBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
