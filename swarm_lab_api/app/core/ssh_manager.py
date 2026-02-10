import paramiko
from typing import List, Dict, Tuple

def execute_remote_command(ip: str, username: str, password: str, command: str) -> Tuple[str, str]:
    """
    Ejecuta un comando remoto en una Raspberry Pi a través de SSH.
    """
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
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        # Cerrar la conexión SSH
        ssh.close()

        return output, error

    except Exception as e:
        raise Exception(f"Error en la conexión o ejecución del comando en {ip}: {str(e)}")

def execute_command_on_multiple_robots(
    robots: List[Dict[str, str]], command: str
) -> List[Dict[str, str]]:
    """
    Ejecuta un comando en múltiples robots definidos en la configuración.
    """
    results = []

    for robot in robots:
        ip = robot.get("host")
        username = robot.get("username")
        password = robot.get("password")

        try:
            output, error = execute_remote_command(ip, username, password, command)
            results.append({
                "ip": ip,
                "status": "success",
                "output": output,
                "error": error
            })
        except Exception as e:
            results.append({
                "ip": ip,
                "status": "failure",
                "error": str(e)
            })

    return results
