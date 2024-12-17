from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.crud.experiments import get_experiment, create_experiment
from app.schemas.experiment import ExperimentCreate, Experiment
from app.db.session import get_db
from app.core.ssh_manager import execute_remote_command
import os
import psutil  # Librería para trabajar con procesos

router = APIRouter()

@router.get("/experiments/{experiment_id}", response_model=Experiment)
def read_experiment(experiment_id: int, db: Session = Depends(get_db)):
    experiment = get_experiment(db, experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment

@router.post("/experiments/", response_model=Experiment)
def create_new_experiment(experiment: ExperimentCreate, db: Session = Depends(get_db)):
    return create_experiment(db, experiment)

class ScriptRequest(BaseModel):
    script_name: str
class ScriptExecutionRequest(BaseModel):
    script_name: str

@router.post("/start-experiment")
async def start_experiment(request: ScriptRequest):
    raspberry_ip = "10.20.50.29"  # Cambia por la IP de tu Raspberry Pi
    raspberry_user = "sphero"  # Usuario de la Raspberry Pi
    raspberry_password = "admin2024"  # Contraseña de la Raspberry Pi

    command = f"python3 scripts/{request.script_name}"

    try:
        # Ejecutar el comando en la Raspberry Pi
        output, error = execute_remote_command(raspberry_ip, raspberry_user, raspberry_password, command)

        if error:
            raise HTTPException(status_code=400, detail=f"Error al ejecutar el script: {error}")

        return {"status": "success", "output": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar o ejecutar el comando: {str(e)}")
    

    # Endpoint para detener el script en la Raspberry Pi
@router.post("/stop-script")
async def stop_script(request: ScriptExecutionRequest):
    # Definir la IP, usuario y contraseña de la Raspberry Pi
    raspberry_ip = "10.20.50.29"  # Cambia por la IP de tu Raspberry Pi
    raspberry_user = "sphero"  # Usuario de la Raspberry Pi
    raspberry_password = "admin2024"  # Contraseña de la Raspberry Pi

    try:
        # Buscar el proceso del script en ejecución
        command = f"pgrep -f {request.script_name}"
        pid_output, error = execute_remote_command(raspberry_ip, raspberry_user, raspberry_password, command)

        if error:
            raise HTTPException(status_code=400, detail=f"Error al obtener el PID: {error}")

        if not pid_output.strip():
            raise HTTPException(status_code=404, detail="No se encontró ningún proceso en ejecución con ese script.")

        # Si se encontró el PID, ejecutamos el comando para detener el proceso
        pid = pid_output.strip()  # Obtener el PID del proceso
        kill_command = f"kill {pid}"  # Comando para detener el proceso
        kill_output, kill_error = execute_remote_command(raspberry_ip, raspberry_user, raspberry_password, kill_command)

        if kill_error:
            raise HTTPException(status_code=400, detail=f"Error al detener el proceso: {kill_error}")

        return {"status": "success", "message": "El script ha sido detenido correctamente."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al intentar detener el script: {str(e)}")