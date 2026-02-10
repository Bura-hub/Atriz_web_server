from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Configuración de la URL de la base de datos desde los settings
DATABASE_URL = settings.DATABASE_URL

# SQLite requiere check_same_thread=False para uso con FastAPI
_connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    _connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=_connect_args)

# Configuración de la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base: DeclarativeMeta = declarative_base()

# Proporciona una sesión de la base de datos para las peticiones
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
