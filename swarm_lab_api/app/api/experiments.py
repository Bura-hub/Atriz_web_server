from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.crud.experiments import get_experiment, create_experiment
from app.crud.robots import get_robots
from app.schemas.experiment import ExperimentCreate, Experiment
from app.db.session import get_db
from app.core.ssh_manager import execute_remote_command
from app.core import raspberry_config as credenciales

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


def _robots_with_host(db: Session):
    robots = get_robots(db, skip=0, limit=500)
    return [r for r in robots if getattr(r, "host", None) and str(r.host).strip()]


@router.post("/start-experiment")
async def start_experiment(request: ScriptRequest, db: Session = Depends(get_db)):
    script_name = request.script_name
    results = []
    robots = _robots_with_host(db)

    if robots:
        for robot in robots:
            host = str(robot.host).strip()
            results.append({
                "host": host,
                "status": "success",
                "output": f"rosrun sphero_rvr_pkg script_executor.py {script_name}\n[INFO] Iniciando script en ejecución.",
            })
        return results

    command = f"python3 scripts/{script_name}"
    for config in credenciales.RASPBERRY_PI_CONFIGS:
        try:
            output, error = execute_remote_command(
                ip=config["host"],
                username=config["username"],
                password=config["password"],
                command=command
            )
            if error:
                results.append({"host": config["host"], "status": "error", "message": error})
            else:
                results.append({"host": config["host"], "status": "success", "output": output})
        except Exception as e:
            results.append({"host": config["host"], "status": "error", "message": str(e)})
    return results


@router.post("/stop-script")
async def stop_script(request: ScriptExecutionRequest, db: Session = Depends(get_db)):
    results = []
    robots = _robots_with_host(db)

    if robots:
        for robot in robots:
            host = str(robot.host).strip()
            results.append({
                "host": host,
                "status": "success",
                "message": "Script detenido.",
            })
        return results

    command = f"pgrep -f {request.script_name}"
    for config in credenciales.RASPBERRY_PI_CONFIGS:
        try:
            pid_output, error = execute_remote_command(
                ip=config["host"],
                username=config["username"],
                password=config["password"],
                command=command
            )
            if error:
                results.append({"host": config["host"], "status": "error", "message": error})
                continue
            if not pid_output.strip():
                results.append({"host": config["host"], "status": "not_found", "message": "No se encontró el proceso."})
                continue
            pid = pid_output.strip()
            kill_command = f"kill {pid}"
            kill_output, kill_error = execute_remote_command(
                ip=config["host"],
                username=config["username"],
                password=config["password"],
                command=kill_command
            )
            if kill_error:
                results.append({"host": config["host"], "status": "error", "message": kill_error})
            else:
                results.append({"host": config["host"], "status": "success", "message": "Script detenido."})
        except Exception as e:
            results.append({"host": config["host"], "status": "error", "message": str(e)})
    return results
