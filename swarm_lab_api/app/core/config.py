from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://admin:123456@localhost/swarm_lab"

    class Config:
        env_file = ".env"

settings = Settings()
