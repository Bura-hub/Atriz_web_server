from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Configuración de la URL de la base de datos desde los settings
DATABASE_URL = settings.DATABASE_URL

# Creación del motor de la base de datos
engine = create_engine(DATABASE_URL)

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
