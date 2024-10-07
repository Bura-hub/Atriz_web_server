import os
import subprocess

def send_code_to_ros(code, robot_ip):
    """
    Envía código Python a una Raspberry Pi remota que ejecuta un nodo ROS.
    
    Args:
        code (str): El código Python a ejecutar.
        robot_ip (str): Dirección IP del robot (Raspberry Pi).
    
    Returns:
        str: Resultado de la ejecución o error.
    """
    try:
        # Guardar el código en un archivo temporal local
        local_script_path = "/tmp/user_script.py"
        with open(local_script_path, "w") as f:
            f.write(code)

        # Transferir el script a la Raspberry Pi usando scp
        remote_script_path = f"{robot_ip}:/tmp/user_script.py"
        scp_command = ["scp", local_script_path, remote_script_path]
        scp_result = subprocess.run(scp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if scp_result.returncode != 0:
            raise Exception(f"Error al transferir script: {scp_result.stderr.decode()}")

        # Ejecutar el script en la Raspberry Pi usando ssh y rosrun
        ssh_command = [
            "ssh", robot_ip,
            "rosrun sphero_rvr_pkg script_executor.py /tmp/user_script.py"
        ]
        ssh_result = subprocess.run(ssh_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if ssh_result.returncode != 0:
            raise Exception(f"Error al ejecutar el script en ROS: {ssh_result.stderr.decode()}")

        return ssh_result.stdout.decode()

    except Exception as e:
        return f"Error: {str(e)}"
