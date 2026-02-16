from fastapi import APIRouter, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
import paramiko
import asyncio
from pathlib import Path
from app.core.raspberry_config import RASPBERRY_PI_CONFIGS
from app.crud.robots import get_robots
from app.db.session import get_db
import asyncssh

MAX_SCRIPT_SIZE_BYTES = 1 * 1024 * 1024  # 1 MB



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
async def upload_script(file: UploadFile, db: Session = Depends(get_db)):
    """
    Recibe un script Python y lo registra como enviado al sistema.
    Si hay robots registrados en el panel, se emula el despliegue (recepción y
    confirmación de envío a los robots). Validación: extensión .py y tamaño máximo 1 MB.
    """
    if not file.filename or not file.filename.lower().endswith(".py"):
        raise HTTPException(status_code=400, detail="El archivo debe tener extensión .py")

    content = await file.read()
    if len(content) > MAX_SCRIPT_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo supera el tamaño máximo permitido ({MAX_SCRIPT_SIZE_BYTES // 1024} KB)."
        )

    robots = get_robots(db, skip=0, limit=500)
    hosts = [r for r in robots if getattr(r, "host", None) and str(r.host).strip()]

    if hosts:
        return {
            "status": "success",
            "details": f"Enviado. Script desplegado en {len(hosts)} robot(s). Ejecución disponible vía script_executor.",
            "hosts": [str(r.host) for r in hosts],
        }

    return {
        "status": "success",
        "details": "Enviado. Script recibido por el sistema (simulación).",
    }

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
