from sqlalchemy.orm import Session
from app.models.robot import Robot
from app.schemas.robot import RobotCreate

def get_robot(db: Session, robot_id: int):
    return db.query(Robot).filter(Robot.id == robot_id).first()

def get_robots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Robot).order_by(Robot.id).offset(skip).limit(limit).all()

def create_robot(db: Session, robot: RobotCreate):
    db_robot = Robot(**robot.dict())
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot

def delete_robot(db: Session, robot_id: int) -> bool:
    robot = get_robot(db, robot_id)
    if robot is None:
        return False
    db.delete(robot)
    db.commit()
    return True
