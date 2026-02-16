from pydantic import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Base de datos: SQLite (desarrollo) o PostgreSQL (producción).
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./swarm_lab.db"
    )
    # JWT: clave para firmar tokens (no incluir en control de versiones).
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cambiar-en-produccion-openssl-rand-hex-32")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    # Duración de la sesión en minutos (doc: 30 o 120 para sesiones largas).
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    # CORS: orígenes permitidos (frontend). Separados por coma en .env.
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8080,http://localhost,http://10.20.50.228,http://atriz-project.duckdns.org"
    )
    # SSH por defecto para robots (usuario del sistema en las Raspberry Pi).
    SSH_USER: str = os.getenv("SSH_USER", "ubuntu")
    # Contraseña SSH opcional; si está vacía se asume autenticación por clave.
    SSH_PASSWORD: str = os.getenv("SSH_PASSWORD", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

settings = Settings()
