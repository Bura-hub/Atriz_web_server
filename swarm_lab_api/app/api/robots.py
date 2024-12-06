from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.crud.robots import get_robot, create_robot
from app.schemas.robot import RobotCreate, Robot
from app.db.session import get_db

router = APIRouter()

@router.get("/robots/{robot_id}", response_model=Robot)
def read_robot(robot_id: int, db: Session = Depends(get_db)):
    robot = get_robot(db, robot_id)
    if robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot

@router.post("/robots/", response_model=Robot)
def create_new_robot(robot: RobotCreate, db: Session = Depends(get_db)):
    return create_robot(db, robot)
