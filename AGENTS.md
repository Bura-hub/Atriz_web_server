# Atriz Web Server / Swarm Lab — Guía para el agente

Proyecto de **laboratorio de robótica swarm** (SW-AR-LabRE): ROS Noetic, API FastAPI (`swarm_lab_api/`), panel Vue 3 (`swarm-robotics-panel/`), PostgreSQL, Nginx. Inicio/parada con `start_atriz_lab.sh` y `stop.sh`.

## Reglas del proyecto

Las instrucciones detalladas están en **`.cursor/rules/`**:

- **project-overview.mdc** (siempre aplicada): stack, estructura de carpetas, puertos, convenciones de idioma y entorno (Linux, ROS, SSH a robots).
- **swarm-api-python.mdc**: estructura de la API FastAPI, patrones (routers, CRUD, schemas, DB, seguridad).
- **ros-and-launch.mdc**: launch files XML, scripts bash del lab, paquetes ROS, comandos en robots.
- **frontend-vue.mdc**: panel Vue 3, componentes, Axios, Tailwind.

Al trabajar en un área concreta, priorizar la regla correspondiente y respetar la estructura y convenciones ya existentes en el código.
