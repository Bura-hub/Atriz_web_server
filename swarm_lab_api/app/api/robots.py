from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from app.crud.robots import get_robot, create_robot
from app.schemas.robot import RobotCreate, Robot
from app.db.session import get_db
import subprocess
import os
import signal

router = APIRouter()
running_processes = {}

@router.get("/robots/{robot_id}", response_model=Robot)
def read_robot(robot_id: int, db: Session = Depends(get_db)):
    robot = get_robot(db, robot_id)
    if robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot

@router.post("/robots/")
def create_new_robot(robot: RobotCreate, db: Session = Depends(get_db)):
    return create_robot(db, robot)

@router.post("/robots/execute/")
async def execute_command_on_robot(robot_ip: str = Form(...), command: str = Form(...)):
    user = os.getenv("SSH_USER", "ubuntu")

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
