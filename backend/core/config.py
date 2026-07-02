"""OrbitOS Backend — Core Configuration"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "OrbitOS"
    APP_ENV: str = "development"
    SECRET_KEY: str = "orbitos-dev-secret-change-in-production"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://orbitos.vercel.app",
        "https://orbitos.ai",
    ]
    
    # Lemma SDK — Core orchestration
    LEMMA_API_KEY: str = ""
    LEMMA_POD_ID: str = ""
    
    # AI Models
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://orbitos:orbitos@localhost:5432/orbitos"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # External Integrations
    GITHUB_TOKEN: str = ""
    GITHUB_ORG: str = ""
    
    SLACK_BOT_TOKEN: str = ""
    SLACK_SIGNING_SECRET: str = ""
    SLACK_DEFAULT_CHANNEL: str = "#general"
    
    GMAIL_CREDENTIALS: str = ""
    GMAIL_TOKEN: str = ""
    
    JIRA_API_TOKEN: str = ""
    JIRA_EMAIL: str = ""
    JIRA_DOMAIN: str = ""
    
    NOTION_TOKEN: str = ""
    NOTION_WORKSPACE_ID: str = ""
    
    GOOGLE_CALENDAR_CREDENTIALS: str = ""
    
    # Auth (Clerk)
    CLERK_SECRET_KEY: str = ""
    CLERK_PUBLISHABLE_KEY: str = ""
    
    # Vector DB
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
