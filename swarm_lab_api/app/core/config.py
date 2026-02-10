from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    # Local: SQLite (sin instalar PostgreSQL). Producción: PostgreSQL.
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./swarm_lab.db"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
