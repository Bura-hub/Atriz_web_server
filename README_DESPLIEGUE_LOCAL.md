# Despliegue local — Atriz Web Server / Swarm Lab

Despliegue de la API FastAPI y del panel Vue en **Windows** (desarrollo local, sin ROS ni Nginx).

## Resumen del análisis

| Componente | Producción (Linux) | Local (Windows) |
|-----------|--------------------|-----------------|
| **API** | Uvicorn puerto 5000, PostgreSQL | Uvicorn puerto 5000, **SQLite** |
| **Frontend** | Build estático servido por Nginx | Dev server Vue en **puerto 8080** |
| **ROS / Nginx / Cámara** | Incluidos en `start_atriz_lab.sh` | No se ejecutan |

## Requisitos

- **Python 3.8+** (recomendado 3.10–3.12)
- **Node.js 18+** y npm
- Opcional: PowerShell (para `start_local.ps1`)

## Opción A: Script automático (PowerShell)

Desde la raíz del proyecto:

```powershell
.\start_local.ps1
```

Se abrirán dos ventanas: una con la API y otra con el frontend.

## Opción B: Manual (dos terminales)

### Terminal 1 — API

```powershell
cd swarm_lab_api
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

### Terminal 2 — Frontend

```powershell
cd swarm-robotics-panel
npm install
npx vue-cli-service serve
```

## URLs locales

| Servicio | URL |
|----------|-----|
| **Panel (Vue)** | http://localhost:8080/ |
| **API** | http://localhost:5000 |
| **Swagger (API)** | http://localhost:5000/admin/docs |
| **ReDoc (API)** | http://localhost:5000/admin/redoc |

## Base de datos local

- Por defecto se usa **SQLite**: `swarm_lab_api/swarm_lab.db`.
- Las tablas se crean al arrancar la API (`Base.metadata.create_all`).
- Para usar PostgreSQL en local, crea `swarm_lab_api/.env` con:
  `DATABASE_URL=postgresql+psycopg2://user:password@localhost/swarm_lab`

## Configuración del frontend

- La API se llama a **http://localhost:5000/api** (definido en `swarm-robotics-panel/src/utils/axios.js`).
- Para otro host/puerto: variable de entorno `VUE_APP_API_URL` (ej. `http://localhost:5000/api`).
- El proxy en `vue.config.js` redirige `/api` al backend cuando usas el dev server (puerto 8080).

## Detener servicios

- Cierra las ventanas/terminales donde están corriendo Uvicorn y Vue, o usa Ctrl+C en cada una.
- En producción Linux se usa `stop.sh`.

## Notas

- **ROS, Nginx y cámara** solo están en el flujo de producción (script `start_atriz_lab.sh` en Linux).
- Los endpoints que usan SSH/ROS (robots, scripts en Raspberry) fallarán si no hay robots accesibles; el resto de la API y el login funcionan en local.
