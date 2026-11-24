"""Application settings loaded from environment variables (never hardcode secrets)."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BACKEND_DIR.parent

# Load .env from the project root first, then allow backend/.env to override.
load_dotenv(PROJECT_DIR / ".env")
load_dotenv(BACKEND_DIR / ".env", override=True)


def _normalize_db_url(url: str) -> str:
    """Accept the legacy 'postgres://' scheme used by some hosting providers."""
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def _optional(name: str) -> str | None:
    value = os.getenv(name, "").strip()
    return value or None


class Settings:
    def __init__(self) -> None:
        self.app_name: str = os.getenv("APP_NAME", "Hare Ram Portfolio API")
        self.app_version: str = "1.0.0"
        self.environment: str = os.getenv("ENVIRONMENT", "development")
        self.database_url: str = _normalize_db_url(
            os.getenv("DATABASE_URL", f"sqlite:///{BACKEND_DIR / 'portfolio.db'}")
        )
        self.cors_origins: list[str] = [
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501"
            ).split(",")
            if origin.strip()
        ]
        # Public profile links. Values set here override the seed data at read time.
        self.linkedin_url: str | None = _optional("PORTFOLIO_LINKEDIN_URL")
        self.github_url: str | None = _optional("PORTFOLIO_GITHUB_URL")
        self.contact_email: str | None = _optional("PORTFOLIO_EMAIL")
        self.resume_path: Path = Path(
            os.getenv("RESUME_PATH", str(BACKEND_DIR / "app" / "static" / "resume.pdf"))
        )
        self.seed_on_startup: bool = os.getenv("SEED_ON_STARTUP", "true").lower() == "true"


@lru_cache
def get_settings() -> Settings:
    return Settings()
