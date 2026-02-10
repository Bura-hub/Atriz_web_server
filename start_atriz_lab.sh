#!/bin/bash

# Configuración de log
LOGFILE="/var/log/swarm_lab.log"
exec > >(tee -a "$LOGFILE") 2>&1

# Función para agregar un timestamp a los mensajes
log() {
    local COLOR_RESET='\033[0m'
    local COLOR_INFO='\033[1;34m'
    local COLOR_SUCCESS='\033[1;32m'
    local COLOR_WARNING='\033[1;33m'
    local COLOR_ERROR='\033[1;31m'
    local MESSAGE_TYPE=$1
    local MESSAGE=$2

    case $MESSAGE_TYPE in
        INFO)    echo -e "${COLOR_INFO}$(date '+%Y-%m-%d %H:%M:%S') - INFO: $MESSAGE${COLOR_RESET}";;
        SUCCESS) echo -e "${COLOR_SUCCESS}$(date '+%Y-%m-%d %H:%M:%S') - SUCCESS: $MESSAGE${COLOR_RESET}";;
        WARNING) echo -e "${COLOR_WARNING}$(date '+%Y-%m-%d %H:%M:%S') - WARNING: $MESSAGE${COLOR_RESET}";;
        ERROR)   echo -e "${COLOR_ERROR}$(date '+%Y-%m-%d %H:%M:%S') - ERROR: $MESSAGE${COLOR_RESET}";;
        *)       echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $MESSAGE";;
    esac
}

# Función para liberar puertos
cleanup_ports() {
    log "INFO" "[LIBERANDO PUERTOS...]"
    fuser -k 8000/tcp
    fuser -k 8080/tcp
    fuser -k 80/tcp
    fuser -k 5000/tcp
}

# Función para finalizar procesos
terminate_processes() {
    log "INFO" "[FINALIZANDO PROCESOS ANTERIORES...]"
    pkill -f roscore
    pkill -f roslaunch
    pkill -f "python3 -m http.server"
    pkill -f usb_cam_node
    pkill -f "uvicorn app.main:app"
}

# Ejecutar la función de finalización de procesos
terminate_processes

# Ejecutar la función de limpieza de puertos
cleanup_ports

# Iniciar ROS core
log "INFO" "[INICIANDO ROSCORE...]"
roscore &
ROSCORE_PID=$!
sleep 5  # Esperar a que roscore esté completamente iniciado
log "SUCCESS" "[ROS core iniciado con PID $ROSCORE_PID.]"

# Iniciar nginx
log "INFO" "[REINICIANDO NGINX...]"
sudo systemctl restart nginx

# Iniciar la cámara USB
log "INFO" "[INICIANDO LA CÁMARA...]"
roslaunch web_server camera.launch &

# Iniciar web_video_server
log "INFO" "[INICIANDO EL WEB_VIDEO_SERVER...]"
roslaunch web_server web_video.launch &

# Iniciar la API de FastAPI con Uvicorn
log "INFO" "[INICIANDO LA API FastAPI...]"
source ~/catkin_ws/swarm_lab_env/bin/activate
cd ~/catkin_ws/swarm_lab_api
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload &

# Construir el proyecto Vue.js
log "INFO" "[CONSTRUYENDO EL PROYECTO Vue.js...]"
cd ~/catkin_ws/swarm-robotics-panel
npm install
npm run build

log "SUCCESS" "[SWARM LAB INICIADO]"
