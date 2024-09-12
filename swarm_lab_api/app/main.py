from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import experiments, robots, users, updates, scripts
from app.db.session import engine, Base
from app.models import experiment, robot, user
from app.dependencies import get_current_user  # Dependencia para la autenticación basada en JWT

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(title="Swarm Robotics Lab API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes de estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)


# Incluir routers para las rutas públicas y protegidas

# Rutas que pueden ser públicas
app.include_router(experiments.router, tags=["Experiments"])
app.include_router(robots.router, tags=["Robots"])
app.include_router(updates.router, tags=["Updates"])
app.include_router(users.router, tags=["Users"])

# Rutas que requieren autenticación
app.include_router(scripts.router, tags=["Scripts"], dependencies=[Depends(get_current_user)])
