from sqlalchemy.orm import Session
from app.models.robot import Robot
from app.schemas.robot import RobotCreate

def get_robot(db: Session, robot_id: int):
    return db.query(Robot).filter(Robot.id == robot_id).first()

def create_robot(db: Session, robot: RobotCreate):
    db_robot = Robot(**robot.dict())
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot
