from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # AI API Keys
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str = ""

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # Environment
    ENVIRONMENT: str = "development"

    # Claude Settings
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7

    # Context Management
    CONTEXT_LIMIT_TOKENS: int = 200000
    CONTEXT_WARNING_THRESHOLD: float = 0.8

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
