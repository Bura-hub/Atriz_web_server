from fastapi import APIRouter
from app.core.ssh_utils import list_scripts_in_all_pis, execute_script_in_all_pis

router = APIRouter()

@router.post("/execute-script")
async def execute_script(script_name: str, remote_directory: str):
    """
    Endpoint para ejecutar un script Python en todas las Raspberry Pi.
    :param script_name: Nombre del script a ejecutar.
    :param remote_directory: Directorio remoto donde se encuentra el script.
    :return: Resultado de la ejecución del script en las Raspberry Pi.
    """
    results = execute_script_in_all_pis(script_name, remote_directory)
    return {"execution_results": results}

@router.get("/list-scripts")
async def list_scripts(remote_directory: str):
    """
    Endpoint para listar los scripts Python en el directorio remoto de todas las Raspberry Pi.
    :param remote_directory: Directorio donde se encuentran los scripts en la Raspberry Pi.
    :return: Diccionario con los scripts disponibles en cada Raspberry Pi.
    """
    scripts = list_scripts_in_all_pis(remote_directory)
    return {"scripts": scripts}