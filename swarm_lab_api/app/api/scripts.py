from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from app.core.ssh_utils import list_scripts_in_all_pis, execute_script_in_all_pis
from app.ros_bridge import send_code_to_ros
import os
import subprocess

router = APIRouter()

@router.post("/scripts/upload/")
async def upload_new_script(file: UploadFile = File(...), robot_ip: str = Form(...)):
    """
    Endpoint para subir y ejecutar un script en una Raspberry Pi con ROS.

    Args:
        file (UploadFile): El archivo Python subido.
        robot_ip (str): La dirección IP del robot (Raspberry Pi).

    Returns:
        dict: Resultado de la ejecución del script.
    """
    user = os.getenv("SSH_USER", "ubuntu")  # Usa el usuario predeterminado
    temp_file_path = "/tmp/script.py"  # Ruta temporal en la Raspberry Pi

    try:
        # Leer el contenido del archivo
        content = await file.read()
        script_content = content.decode()

        # Guardar el contenido en un archivo temporal en la Raspberry Pi
        with open(temp_file_path, 'wb') as f:
            f.write(content)

        # Cambiar permisos para hacer el script ejecutable
        subprocess.run(["ssh", f"{user}@{robot_ip}", f"chmod +x {temp_file_path}"])

        # Ejecutar el script en la Raspberry Pi
        execution_result = send_code_to_ros(temp_file_path, robot_ip, user)

        return {"status": "success", "result": execution_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar el script: {str(e)}")

@router.post("/execute-script")
async def execute_script(script_name: str):
    """
    Endpoint para ejecutar un script Python en todas las Raspberry Pi.
    :param script_name: Nombre del script a ejecutar.
    :return: Resultado de la ejecución del script en las Raspberry Pi.
    """
    results = execute_script_in_all_pis(script_name)
    return {"execution_results": results}

@router.get("/list-scripts")
async def list_scripts():
    """
    Endpoint para listar los scripts Python en el directorio remoto de todas las Raspberry Pi.
    :return: Diccionario con los scripts disponibles en cada Raspberry Pi.
    """
    scripts = list_scripts_in_all_pis()
    return {"scripts": scripts}