from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

# Load .env.local explicitly before creating Settings
env_path = Path(__file__).parent / ".env.local"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_JWT_SECRET: str  # Don't forget this one if you need it

    # Gemini AI Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-pro"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 2048

    class ConfigDict:
        env_file = ".env.local"
        env_file_encoding = 'utf-8'

settings = Settings()