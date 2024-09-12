#!/bin/bash

# Función para liberar puertos
cleanup_ports() {
    echo "LIBERANDO PUERTOS..."
    fuser -k 8000/tcp
    fuser -k 8080/tcp
    fuser -k 80/tcp
    fuser -k 5000/tcp  # Añadir el puerto 5000 si no estaba
}

# Función para finalizar procesos
terminate_processes() {
    echo "Finalizando procesos anteriores..."
    pkill -f roscore
    pkill -f roslaunch
    pkill -f "python3 -m http.server"
    pkill -f usb_cam_node
    pkill -f "uvicorn app.main:app"  # Detener FastAPI si ya está corriendo
}

# Ejecutar la función de finalización de procesos
terminate_processes

# Ejecutar la función de limpieza de puertos
cleanup_ports

# Iniciar ROS core
echo "Iniciando roscore..."
roscore &
ROSCORE_PID=$!
sleep 5  # Esperar a que roscore esté completamente iniciado

# Iniciar nginx
sudo systemctl restart nginx

# Iniciar la cámara USB
echo "Iniciando la Camara..."
roslaunch web_server camera.launch &

# Iniciar web_video_server
echo "Iniciando el Web_server..."
roslaunch web_server web_video.launch &

# Iniciar la API de FastAPI con Uvicorn
echo "Iniciando la API FastAPI..."
source ~/catkin_ws/swarm_lab_env/bin/activate
cd ~/catkin_ws/swarm_lab_api
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload &

# Construir el proyecto Vue.js
echo "Construyendo el proyecto Vue.js..."
cd ~/catkin_ws/swarm-robotics-panel
npm install
npm run build

echo "SWARM LAB INICIADO"
