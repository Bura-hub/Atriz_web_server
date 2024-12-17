import paramiko
import time
from typing import Tuple

def execute_remote_command(ip: str, username: str, password: str, command: str) -> Tuple[str, str]:
    try:
        # Conectar a la Raspberry Pi a través de SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        # Activar entorno ROS y ejecutar el comando
        command_with_ros = f"source /opt/ros/noetic/setup.bash && source ~/atriz_git/devel/setup.bash && {command}"

        # Ejecutar el comando
        stdin, stdout, stderr = ssh.exec_command(command_with_ros, timeout=4.0)

        # Leer la salida y error
        output = stdout.read().decode()
        error = stderr.read().decode()

        # Esperar 3 segundos antes de cerrar la conexión para evitar Timeouts
        #time.sleep(3)

        # Cerrar la conexión SSH
        ssh.close()

        return output, error

    except Exception as e:
        raise Exception(f"Error en la conexión o ejecución del comando: {str(e)}")
