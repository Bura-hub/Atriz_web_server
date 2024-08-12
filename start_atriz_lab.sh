#!/bin/bash

# Función para liberar puertos
cleanup_ports() {
    echo "LIBERANDO PUERTOS..."
    fuser -k 8000/tcp
    fuser -k 8080/tcp
    # Agrega más puertos si es necesario
}

# Función para finalizar procesos
terminate_processes() {
    echo "Finalizando procesos anteriores..."
    pkill -f roscore
    pkill -f roslaunch
    pkill -f "python3 -m http.server"
    pkill -f usb_cam_node
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

# Iniciar la cámara USB
echo "Iniciando la Camara..."
roslaunch web_server camera.launch &

# Iniciar web_video_server
echo "Iniciando el Web_server..."
roslaunch web_server web_video.launch &

# Iniciar el servidor web para el cliente (usando Python para simplicidad)
cd ~/catkin_ws/web_client
python3 -m http.server 8000 &

echo "Swarm Lab iniciado. Accede al cliente web en http://localhost:8000"
