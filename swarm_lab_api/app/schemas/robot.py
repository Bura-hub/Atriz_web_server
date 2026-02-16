from pydantic import BaseModel
from typing import Optional

class RobotBase(BaseModel):
    name: str
    type: str
    host: Optional[str] = None  # IP address (e.g. 10.20.50.231)

class RobotCreate(RobotBase):
    pass

class Robot(RobotBase):
    id: int

    class Config:
        orm_mode = True
