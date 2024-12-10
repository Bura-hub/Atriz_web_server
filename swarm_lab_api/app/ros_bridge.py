import subprocess

def send_code_to_ros(script_path: str, robot_ip: str, user: str):
    """
    Envía un script Python a la Raspberry Pi y lo ejecuta.

    Args:
        script_path (str): La ruta del script a ejecutar.
        robot_ip (str): La dirección IP del robot (Raspberry Pi).
        user (str): El usuario SSH.

    Returns:
        str: La salida de la ejecución del script.
    
    Raises:
        Exception: Si ocurre un error al ejecutar el script.
    """
    try:
        # Comando que incluye el sourcing de ROS y la ejecución del script
        ssh_command = ["ssh", f"{user}@{robot_ip}", f"source /opt/ros/noetic/setup.bash; python3 {script_path}"]

        # Ejecutar el comando
        result = subprocess.run(ssh_command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Error en la ejecución del script: {result.stderr}")
        
        return result.stdout

    except Exception as e:
        raise Exception(f"Error al enviar el script al robot: {str(e)}")
