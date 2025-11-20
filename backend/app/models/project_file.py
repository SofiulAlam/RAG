from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class ProjectFile(Base):
    __tablename__ = "project_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    path = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(50))
    is_locked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="files")

    __table_args__ = (
        UniqueConstraint("project_id", "path", name="uix_project_file_path"),
    )
