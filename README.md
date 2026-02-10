# Atriz Web Server / Swarm Lab

Laboratorio de robótica swarm (SW-AR-LabRE): panel web Vue 3, API FastAPI, integración con ROS y robots (Sphero RVR, Raspberry Pi).

## Instalación y ejecución (quien clone el repo)

Para **instalar y ejecutar la aplicación** después de clonar:

1. **Requisitos:** Python 3.8+ (recomendado 3.10–3.12), Node.js 18+ y npm.

2. **Opción rápida (Windows con PowerShell):**
   ```powershell
   .\start_local.ps1
   ```
   Se abren la API y el frontend automáticamente.

3. **Opción manual (cualquier sistema):**
   - **Terminal 1 – API:**  
     `swarm_lab_api/` → crear venv, activar, `pip install -r requirements.txt`, `uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload`  
     (detalle en [swarm_lab_api/COMO_EJECUTAR.md](swarm_lab_api/COMO_EJECUTAR.md)).
   - **Terminal 2 – Panel:**  
     `swarm-robotics-panel/` → `npm install`, `npm run serve`.

4. **URLs:** Panel en http://localhost:8080/, API en http://localhost:5000 (docs en `/admin/docs` y `/admin/redoc`).

Instrucciones completas de despliegue local (Windows, base de datos, proxy): **[README_DESPLIEGUE_LOCAL.md](README_DESPLIEGUE_LOCAL.md)**.

## Estructura principal

| Carpeta / archivo        | Descripción                          |
|--------------------------|--------------------------------------|
| `swarm-robotics-panel/`  | Frontend Vue 3 (panel de control)    |
| `swarm_lab_api/`         | API FastAPI (auth, experimentos, robots) |
| `start_atriz_lab.sh`    | Arranque en Linux (ROS, Nginx, API, panel) |
| `start_local.ps1`       | Arranque local Windows               |
| `docs/`                 | Documentación (desarrollo, driver, manual) |

## Producción (Linux)

En entorno con ROS y Nginx se usa `start_atriz_lab.sh`; parada con `stop.sh`. Ver [AGENTS.md](AGENTS.md) y reglas en `.cursor/rules/` para más contexto del proyecto.
