from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import experiments, robots, users, updates, scripts
from app.db.session import engine, Base
from app.models import experiment, robot, user
from app.dependencies import get_current_user  # Dependencia para la autenticación basada en JWT

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="Swarm Robotics Lab API",
    openapi_url="/admin/openapi.json",
    docs_url="/admin/docs",  # Cambiar la ruta de Swagger UI
    redoc_url="/admin/redoc"  # Cambiar la ruta de ReDoc (opcional)
)


# Configuración de CORS
origins = [
    "http://atriz-project.duckdns.org",  # Añade aquí el origen de tu frontend
    "http://localhost",  # Si estás probando desde localhost
    "http://localhost:8080",  # Si usas Vue CLI en localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
