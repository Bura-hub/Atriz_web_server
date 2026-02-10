#!/bin/bash

# Función para liberar puertos
cleanup_ports() {
    echo "LIBERANDO PUERTOS..."
    fuser -k 8000/tcp
    fuser -k 8080/tcp
    fuser -k 80/tcp
}

# Función para finalizar procesos
terminate_processes() {
    echo "Finalizando procesos..."
    pkill -f roscore
    pkill -f roslaunch
    pkill -f usb_cam_node
    pkill -f web_video_server
    sudo systemctl stop nginx  # Detener Nginx
}

# Ejecutar las funciones
terminate_processes
cleanup_ports

echo "Todos los servicios han sido detenidos."
