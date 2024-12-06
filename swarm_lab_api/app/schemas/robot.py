from pydantic import BaseModel

class RobotBase(BaseModel):
    name: str
    type: str

class RobotCreate(RobotBase):
    pass

class Robot(RobotBase):
    id: int

    class Config:
        orm_mode = True
