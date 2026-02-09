# SW-LRE-UDENAR

**Software del Laboratorio de Robótica de Enjambres de la Universidad de Nariño**

Plataforma web para orquestar, controlar y monitorear experimentos con robots tipo Sphero RVR en un laboratorio remoto y abierto de robótica de enjambres.

---

## Descripción

SW-LRE-UDENAR es el software central del **Laboratorio de Robótica de Enjambres (LRE-UDENAR)** de la Universidad de Nariño. Permite a investigadores y estudiantes ejecutar experimentos con múltiples robots Sphero RVR desde un navegador, sin gestionar manualmente conexiones SSH, túneles de red ni la compilación de paquetes ROS.

El sistema actúa como un **orquestador de middleware** que integra:

- Una **interfaz web** (Vue.js 3) para login, control de experimentos, envío de scripts y visualización de vídeo y sensores.
- Un **servidor de aplicación** (FastAPI) con API REST, autenticación JWT y módulo de integración con los robots vía SSH/SCP.
- **Agentes robóticos** (Raspberry Pi + ROS Noetic + driver Atriz para Sphero RVR) que ejecutan el código y publican telemetría.

El desarrollo se enmarca en el proyecto N.º 2703 *"Desarrollo de un laboratorio remoto y abierto en la línea de robótica de enjambres para la Universidad de Nariño"* (Convocatoria Docente 2022), con apoyo de la Vicerrectoría de Investigaciones e Interacción Social (VIIS) y el Grupo de Investigación en Ingeniería Eléctrica y Electrónica (GIIEE).

---

## Características principales

- **Acceso web unificado**: login con JWT, dashboard y rutas protegidas por guards.
- **Control de experimentos**: inicio, parada y reinicio de sesiones; envío de scripts Python a los robots.
- **Ejecución remota de scripts**: carga de archivos `.py`, transferencia por SCP y ejecución en el robot vía `rosrun sphero_rvr_pkg script_executor.py`.
- **Visualización de vídeo**: stream MJPEG desde cámaras USB de los robots (`web_video_server`).
- **API REST**: CRUD de usuarios, gestión de robots y experimentos; documentación interactiva en `/admin/docs`.
- **Driver ROS (Atriz)**: nodo que reconcilia `rospy` (síncrono) con el SDK asyncio del Sphero RVR; tópicos estándar (`/cmd_vel`, odometría, IMU) y mensajes personalizados (`atriz_rvr_msgs`).
- **Seguridad operacional**: failsafe por timeout, heartbeat y parada de emergencia (E-Stop) desde la interfaz.

---

## Arquitectura

```
┌─────────────────┐     HTTPS / API REST      ┌─────────────────────┐     SSH/SCP      ┌──────────────────────────┐
│   Navegador     │ ◄──────────────────────► │   Servidor (FastAPI) │ ◄──────────────► │  Raspberry Pi + ROS       │
│   Vue.js 3      │     JWT, MJPEG (directo   │   PostgreSQL         │   ros_bridge     │  Sphero RVR + usb_cam    │
│   Axios, Router │      al robot :8080)      │   Nginx              │                  │  atriz_rvr_driver        │
└─────────────────┘                           └─────────────────────┘                  └──────────────────────────┘
```

- **Cliente**: SPA Vue.js 3, Axios, visualización MJPEG.
- **Servidor**: FastAPI (Python 3.8+), Uvicorn/Gunicorn, SQLAlchemy, bcrypt, JWT; módulo `ros_bridge.py` para SSH/SCP.
- **Robot**: Ubuntu 20.04, ROS Noetic, driver en tres capas (UART/protocolo Sphero, adapter/State Buffer, nodo rospy con `/cmd_vel` y publicación de sensores).

---

## Stack tecnológico

| Capa        | Tecnología |
|------------|------------|
| Frontend   | Vue.js 3, Vue Router, Axios, Monaco Editor (opcional) |
| Backend    | FastAPI, Uvicorn, Pydantic, SQLAlchemy |
| Base de datos | PostgreSQL |
| Servidor web | Nginx (producción) |
| Robot      | Raspberry Pi 4/3 B+, Ubuntu 20.04, ROS Noetic, Python 3 (asyncio + rospy) |
| Hardware   | Sphero RVR, cámara USB, UART 115200 baud |

---

## Requisitos

- **Servidor**: Python 3.8+, PostgreSQL, Nginx (o equivalente).
- **Robots**: Raspberry Pi 4 o 3 B+ con Ubuntu 20.04, ROS Noetic, paquete Sphero SDK para Raspberry Pi, red accesible desde el servidor (IPs estáticas recomendadas).
- **Red**: WiFi estable; preferible 5 GHz para vídeo y control.

---

## Configuración y despliegue (resumen)

### Backend

1. Clonar el repositorio e instalar dependencias: `pip install -r requirements.txt`.
2. Configurar variables de entorno en `.env` (no versionar):
   - `DATABASE_URL` (PostgreSQL)
   - `SECRET_KEY` (JWT, p. ej. `openssl rand -hex 32`)
   - `ALGORITHM` (HS256), `ACCESS_TOKEN_EXPIRE_MINUTES`
   - `ROBOT_SSH_USER`, `ROBOT_SSH_KEY_PATH`
3. Crear base de datos y usuario PostgreSQL; inicializar esquema (`app/db/init_db.py` o Alembic).
4. Ejecutar en producción:  
   `gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app`

### Frontend

1. `npm install` y `npm run build`.
2. Copiar `dist/` al servidor (p. ej. `/var/www/atriz_frontend`).
3. Configurar Nginx: raíz para estáticos Vue, `location /api` con `proxy_pass` al backend (puerto 8000). Usar `try_files $uri $uri/ /index.html` para Vue Router en modo history.

### Robots (Raspberry Pi)

1. Instalar Ubuntu 20.04 y ROS Noetic.
2. Liberar UART (deshabilitar consola serial en `/boot/config.txt` o `/boot/firmware/config.txt`).
3. Clonar y compilar el workspace del driver (Atriz RVR); añadir usuario al grupo `dialout`.
4. Asegurar SSH: clave pública del servidor en el robot; `ROBOT_SSH_KEY_PATH` apuntando a la clave privada en el servidor.

La documentación detallada de desarrollo, despliegue y variables de entorno está en los documentos LaTeX del repositorio (véase **Documentación**).

---

## Documentación

En este repositorio se incluyen:

| Documento | Contenido |
|----------|-----------|
| **Documento de Desarrollo** | Arquitectura, driver ROS (capas, concurrencia, cinemática), servidor web (FastAPI, `ros_bridge`, JWT), integración end-to-end, configuración, pruebas, seguridad y limitaciones. |
| **Manual de Usuario** | Acceso a la plataforma, uso de la interfaz (login, control de experimentos, vídeo, API de usuarios), resolución de problemas. |
| **Driver ROS para Sphero RVR** | Análisis técnico del driver: protocolo, UART, máquina de estados, checksum, riesgos. |

Los PDF compilados (si se generan) pueden ubicarse en la raíz o en carpetas `docs/` según la organización del repo.

---
*(La estructura real puede variar; el driver ROS puede vivir en un workspace catkin separado.)*

---

## Limitaciones y consideraciones

- **Vídeo**: MJPEG sobre HTTP; latencia típica 200–500 ms. No apto para teleoperación de alta velocidad. Se recomienda reducir resolución, calidad y fps en `web_video_server` y usar WiFi 5 GHz.
- **Odometría**: Basada en encoders del RVR; puede haber deriva por deslizamiento. No se aplica fusión de sensores avanzada (p. ej. EKF) en el servidor.
- **Escalabilidad**: La orquestación depende de conexiones SSH/SCP desde el backend; la escalabilidad está ligada al número de conexiones simultáneas y a la red.
- **Seguridad**: El stream MJPEG (puerto 8080) en configuración estándar puede no estar cifrado ni protegido por autenticación. La ejecución de scripts subidos por usuarios asume un entorno de confianza (laboratorio académico).

---

## Autores

- **Brayan Stiven López-Méndez** — [bsmendez24B@udenar.edu.co](mailto:bsmendez24B@udenar.edu.co) — Ing. Electrónico, Estudiante Maestría en Ingeniería Electrónica, Universidad de Nariño  
- **Wilson Olmedo Achicanoy-Martínez, PhD.** — [wilachic@udenar.edu.co](mailto:wilachic@udenar.edu.co) — Docente Tiempo Completo, Departamento de Electrónica, Universidad de Nariño  

---

## Agradecimientos

Universidad de Nariño, Vicerrectoría de Investigaciones e Interacción Social (VIIS), Grupo de Investigación en Ingeniería Eléctrica y Electrónica (GIIEE), y todos los investigadores del Departamento de Electrónica involucrados en el proyecto del Laboratorio de Robótica de Enjambres.

---

## Licencia

Consulte el repositorio o la documentación del proyecto para información sobre la licencia de uso y distribución.
