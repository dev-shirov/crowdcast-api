from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from src.models import models
from src.models.database import get_db
from src.models.schemas import query_predictions


router = APIRouter()


@router.get("/predictions", response_model=Dict[str, list[models.PredictionsModel]])
def get_predictions(db: Session = Depends(get_db)):
    prediction = query_predictions(db)

    if prediction is None:
        raise HTTPException(status_code=404, detail="Predictions not found!")

    return prediction
