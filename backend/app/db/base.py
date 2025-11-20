from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for Alembic
from app.models.user import User  # noqa
from app.models.project import Project  # noqa
from app.models.chat_message import ChatMessage  # noqa
from app.models.project_file import ProjectFile  # noqa
from app.models.template import Template  # noqa
