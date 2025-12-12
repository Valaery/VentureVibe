from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os
from pathlib import Path

# Get the project root directory (parent of backend/)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Venture Vibe"
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "venture_vibe"
    SECRET_KEY: str = "your-secret-key-change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: str = "https://openrouter.ai/api/v1"
    LLM_MODEL: str = "openai:google/gemini-2.5-flash-lite"

    model_config = ConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding='utf-8',
        extra='ignore'  # Allow extra fields in .env without validation errors
    )

settings = Settings()
