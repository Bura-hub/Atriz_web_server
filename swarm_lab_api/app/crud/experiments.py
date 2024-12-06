from sqlalchemy.orm import Session
from app.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate

def get_experiment(db: Session, experiment_id: int):
    return db.query(Experiment).filter(Experiment.id == experiment_id).first()

def create_experiment(db: Session, experiment: ExperimentCreate):
    db_experiment = Experiment(**experiment.dict())
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment
