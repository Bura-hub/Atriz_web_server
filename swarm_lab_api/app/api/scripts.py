from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.crud.scripts import upload_script
from app.ros_bridge import send_code_to_ros

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
    try:
        # Leer el contenido del archivo
        content = await file.read()
        script_content = content.decode()

        # Subir el script al sistema de almacenamiento (opcional)
        upload_script(script_content)

        # Enviar el script al robot y ejecutarlo
        execution_result = send_code_to_ros(script_content, robot_ip)
        
        return {"status": "success", "result": execution_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar el script: {str(e)}")
