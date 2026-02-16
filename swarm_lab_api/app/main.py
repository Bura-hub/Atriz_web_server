import asyncio
import logging

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import experiments, robots, users, updates, scripts, files
from app.db.session import engine, Base, SessionLocal
from app.models import experiment, robot, user
from app.core.config import settings
from app.dependencies import get_current_user  # Dependencia para la autenticación basada en JWT
from app.crud.users import create_user, get_user_by_username
from app.schemas.user import UserCreate


class SuppressReloadShutdownErrorsFilter(logging.Filter):
    """Evita que el reload de Uvicorn llene la consola con CancelledError/KeyboardInterrupt."""
    def filter(self, record):
        if record.exc_info and record.exc_info[0] is not None:
            exc_type = record.exc_info[0]
            if issubclass(exc_type, (asyncio.CancelledError, KeyboardInterrupt)):
                return False
        return True


# Aplicar filtro para no mostrar tracebacks de reinicio por --reload
for name in ("uvicorn.error", "uvicorn", ""):
    log = logging.getLogger(name) if name else logging.getLogger()
    log.addFilter(SuppressReloadShutdownErrorsFilter())

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)


def init_default_user():
    """Crea un usuario por defecto si no existe ninguno (solo para desarrollo/primer arranque)."""
    db = SessionLocal()
    try:
        if get_user_by_username(db, "admin") is None:
            create_user(db, UserCreate(username="admin", password="admin", full_name="Administrador"))
    finally:
        db.close()

# Crear la aplicación FastAPI (SW-LRE-UDENAR / Plataforma Atriz)
app = FastAPI(
    title="SW-LRE-UDENAR API",
    description="API del Laboratorio de Robótica de Enjambres - Universidad de Nariño (Plataforma Atriz)",
    openapi_url="/admin/openapi.json",
    docs_url="/admin/docs",
    redoc_url="/admin/redoc",
)


def ensure_robot_host_column():
    """Añade la columna host a la tabla robots si no existe (migración en caliente)."""
    from sqlalchemy import text
    if not settings.DATABASE_URL.startswith("sqlite"):
        return
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE robots ADD COLUMN host VARCHAR(255)"))
            conn.commit()
    except Exception:
        pass  # Columna ya existe o tabla no existe aún

@app.on_event("startup")
def on_startup():
    init_default_user()
    ensure_robot_host_column()


# CORS: orígenes desde config (CORS_ORIGINS en .env)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers para las rutas públicas y protegidas

# Rutas que pueden ser públicas
app.include_router(experiments.router, prefix="/api", tags=["Experiments"])
app.include_router(robots.router, prefix="/api", tags=["Robots"])
app.include_router(updates.router, prefix="/api", tags=["Updates"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(scripts.router, prefix="/api", tags=["Scripts"])
app.include_router(files.router, prefix="/api", tags=["Files"])