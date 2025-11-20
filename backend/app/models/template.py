from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.base import Base


class Template(Base):
    __tablename__ = "prompt_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    description = Column(Text)
    template_prompt = Column(Text, nullable=False)
    framework = Column(String(50))
    preview_image = Column(String(500))
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
