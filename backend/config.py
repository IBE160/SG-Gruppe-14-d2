from __future__ import annotations

from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


# Absolute path to backend/.env.local
ENV_PATH = Path(__file__).parent / ".env.local"

# Load it into process env so *everything* can read it (incl. libraries)
# override=False means real environment variables win (good for CI / deployment)
load_dotenv(dotenv_path=ENV_PATH, override=False)


class Settings(BaseSettings):
    # Tell pydantic-settings to also read the same env file (absolute path = robust)
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Supabase ---
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str

    # Optional: only needed if you later choose to verify JWT locally
    SUPABASE_JWT_SECRET: Optional[str] = None

    # --- Gemini ---
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-pro"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 2048


settings = Settings()
