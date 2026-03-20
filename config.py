"""
Configuration — loaded from environment variables / .env
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., description="Telegram Bot Token")
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:password@localhost:5432/orthodox_bot",
        description="PostgreSQL async DSN",
    )
    ADMIN_IDS: list[int] = Field(
        default=[],
        description="Telegram user IDs with full admin access (comma-separated in env)",
    )
    GOOGLE_MAPS_API_KEY: str = Field(default="", description="Google Maps API key")
    # Rate limiting for user questions
    QUESTION_COOLDOWN_HOURS: int = Field(default=24)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
