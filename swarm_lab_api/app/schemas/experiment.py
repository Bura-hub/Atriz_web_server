from pydantic import BaseModel

class ExperimentBase(BaseModel):
    name: str
    description: str

class ExperimentCreate(ExperimentBase):
    pass

class Experiment(ExperimentBase):
    id: int

    class Config:
        orm_mode = True
