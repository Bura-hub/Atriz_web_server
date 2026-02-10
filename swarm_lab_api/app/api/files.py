from fastapi import APIRouter, UploadFile, HTTPException
import paramiko
import asyncio
from pathlib import Path
from app.core.raspberry_config import RASPBERRY_PI_CONFIGS  # Importar las configuraciones
import asyncssh



# Crear un router para manejar las rutas relacionadas con archivos
router = APIRouter()

async def execute_ssh_command_async(host: str, username: str, password: str, command: str):
    """
    Ejecuta un comando SSH de forma asíncrona en una Raspberry Pi.
    """
    try:
        async with asyncssh.connect(
            host, username=username, password=password
        ) as conn:
            result = await conn.run(command, check=True)
            output = result.stdout.strip()
            error = result.stderr.strip()
            
            if error:
                return {"status": "error", "details": error}
            return {"status": "success", "details": output}
    except Exception as e:
        return {"status": "error", "details": str(e)}
    
@router.post("/execute-script")
async def execute_script(script_name: str):
    """
    Ejecuta un script Python en todas las Raspberry Pi configuradas de manera asíncrona.
    """
    if not script_name.endswith(".py"):
        raise HTTPException(status_code=400, detail="El nombre del script debe terminar en .py.")
    
    command = f"python3 scripts/{script_name}"
    
    # Crear tareas asíncronas para ejecutar en paralelo
    tasks = [
        execute_ssh_command_async(
            config["host"], config["username"], config["password"], command
        )
        for config in RASPBERRY_PI_CONFIGS
    ]
    
    # Esperar a que todas las tareas terminen
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Procesar los resultados y capturar cualquier error
    response = []
    for config, result in zip(RASPBERRY_PI_CONFIGS, results):
        if isinstance(result, Exception):
            response.append({
                "host": config["host"],
                "result": {"status": "error", "details": str(result)}
            })
        else:
            response.append({
                "host": config["host"],
                "result": result
            })
    
    return {"results": response}

@router.post("/upload-script")
async def upload_script(file: UploadFile):
    """
    Sube un archivo de script a todas las Raspberry Pi configuradas.
    """
    # Guardar temporalmente el archivo en el servidor
    temp_dir = Path("/tmp")
    temp_path = temp_dir / file.filename
    with temp_path.open("wb") as temp_file:
        temp_file.write(await file.read())

    # Enviar el archivo a cada Raspberry Pi
    for config in RASPBERRY_PI_CONFIGS:
        try:
            remote_dir = f"/home/{config['username']}/scripts"
            remote_path = f"{remote_dir}/{file.filename}"
            send_file_to_pi(config, str(temp_path), remote_dir, remote_path)
        except Exception as e:
            return {
                "status": "error",
                "details": f"Error enviando a {config['host']}: {str(e)}"
            }
    
    return {"status": "success", "details": "Archivo enviado a todas las Raspberry Pi."}

def send_file_to_pi(config, local_path, remote_dir, remote_path):
    """
    Sube un archivo local a una Raspberry Pi remota usando SFTP.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config['host'], username=config['username'], password=config['password'])

    sftp = ssh.open_sftp()

    # Crear la carpeta remota si no existe
    try:
        sftp.stat(remote_dir)  # Verificar si la carpeta existe
    except FileNotFoundError:
        sftp.mkdir(remote_dir)  # Crear la carpeta si no existe

    # Subir el archivo
    sftp.put(local_path, remote_path)
    sftp.close()
    ssh.close()
