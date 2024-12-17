from fastapi import APIRouter, UploadFile, HTTPException
import paramiko
from pathlib import Path

# Definir la configuración de las Raspberry Pi
RASPBERRY_PI_CONFIGS = [
    {"host": "10.20.50.29", "username": "sphero", "password": "admin2024"},
    # {"host": "192.168.1.102", "username": "pi", "password": "raspberry"},
    # Añade más Raspberry Pi aquí
]

# Crear un router para manejar las rutas relacionadas con archivos
router = APIRouter()

def execute_ssh_command(host, username, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password)
        
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        client.close()
        if error:
            return {"status": "error", "details": error}
        return {"status": "success", "details": output}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@router.post("/execute-script")
async def execute_script(script_name: str):
    if not script_name.endswith(".py"):
        raise HTTPException(status_code=400, detail="El nombre del script debe terminar en .py.")
    
    command = f"python3 scripts/{script_name}"
    results = []
    
    for config in RASPBERRY_PI_CONFIGS:
        result = execute_ssh_command(
            host=config["host"],
            username=config["username"],
            password=config["password"],
            command=command
        )
        results.append({"host": config["host"], "result": result})
    
    return {"results": results}

@router.post("/upload-script")
async def upload_script(file: UploadFile):
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
            return {"status": "error", "details": f"Error enviando a {config['host']}: {e}"}
    
    return {"status": "success", "details": "Archivo enviado a todas las Raspberry Pi."}

def send_file_to_pi(config, local_path, remote_dir, remote_path):
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