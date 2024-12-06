from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.crud.experiments import get_experiment, create_experiment
from app.schemas.experiment import ExperimentCreate, Experiment
from app.db.session import get_db

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
