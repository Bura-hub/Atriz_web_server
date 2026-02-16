from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app.crud.robots import get_robot, get_robots, create_robot, delete_robot
from app.schemas.robot import RobotCreate, Robot
from app.db.session import get_db
from app.core.config import settings
import subprocess
import signal

router = APIRouter()
running_processes = {}

@router.get("/robots/", response_model=list[Robot])
def list_robots(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_robots(db, skip=skip, limit=limit)

@router.get("/robots/ssh-defaults")
def get_ssh_defaults():
    """Credenciales SSH por defecto del sistema (solo usuario; la contraseña no se expone)."""
    return {
        "username": settings.SSH_USER,
        "auth_note": "key" if not settings.SSH_PASSWORD else "password",
    }

@router.get("/robots/{robot_id}", response_model=Robot)
def read_robot(robot_id: int, db: Session = Depends(get_db)):
    robot = get_robot(db, robot_id)
    if robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot

@router.post("/robots/", response_model=Robot)
def create_new_robot(robot: RobotCreate, db: Session = Depends(get_db)):
    return create_robot(db, robot)

@router.delete("/robots/{robot_id}")
def remove_robot(robot_id: int, db: Session = Depends(get_db)):
    if not delete_robot(db, robot_id):
        raise HTTPException(status_code=404, detail="Robot not found")
    return {"status": "success", "message": "Robot eliminado."}

@router.post("/robots/execute/")
async def execute_command_on_robot(robot_ip: str = Form(...), command: str = Form(...)):
    user = settings.SSH_USER

    try:
        # Comando que incluye el sourcing de ROS
        ssh_command = ["ssh", f"{user}@{robot_ip}", 
                       f"source /opt/ros/noetic/setup.bash; source ~/atriz_git/devel/setup.bash; {command}"]
        
        # Iniciar el comando en segundo plano
        process = subprocess.Popen(ssh_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Guardar el proceso en el diccionario
        running_processes[robot_ip] = process

        stdout, stderr = process.communicate()  # Espera hasta que el proceso termine
        return {"status": "success", "result": stdout.decode()}

    except Exception as e:
        print(f"Error en el endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al ejecutar el comando: {str(e)}")

@router.post("/robots/stop/")
async def stop_command_on_robot(robot_ip: str = Form(...)):
    if robot_ip in running_processes:
        process = running_processes[robot_ip]
        process.send_signal(signal.SIGINT)  # Enviar Ctrl+C
        process.wait()  # Esperar que el proceso termine
        del running_processes[robot_ip]  # Eliminar el proceso del diccionario
        return {"status": "success", "message": "Comando detenido."}
    else:
        raise HTTPException(status_code=404, detail="No hay comando en ejecución para este robot.")


@router.post("/robots/emergency-stop/")
async def emergency_stop_robot(robot_ip: str = Form(...)):
    """
    Parada de emergencia (E-Stop): publica en /rvr/emergency_stop en el robot
    para cortar potencia y sobrescribir comandos según el driver.
    """
    user = settings.SSH_USER
    # std_msgs/Empty: rostopic pub -1 /rvr/emergency_stop std_msgs/Empty "{}"
    command = "rostopic pub -1 /rvr/emergency_stop std_msgs/Empty '{}'"
    try:
        ssh_cmd = [
            "ssh", f"{user}@{robot_ip}",
            f"source /opt/ros/noetic/setup.bash; source ~/atriz_git/devel/setup.bash; {command}"
        ]
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            raise HTTPException(
                status_code=502,
                detail=f"Error en el robot: {result.stderr or result.stdout or 'unknown'}"
            )
        return {"status": "success", "message": "Parada de emergencia enviada."}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Timeout al contactar con el robot.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar parada de emergencia: {str(e)}")
