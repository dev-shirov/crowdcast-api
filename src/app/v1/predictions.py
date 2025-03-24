from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Optional

from src.models import models
from src.models.database import get_db
from src.models.schemas import  query_recommendation, query_predictions


router = APIRouter()


@router.get("/predictions", response_model=Dict[str, list[models.PredictionsModel]])
def get_predictions(month: Optional[int] = None, location: Optional[str] = None, db: Session = Depends(get_db)):
    predictions = query_predictions(month, location, db)

    if predictions is None:
        raise HTTPException(status_code=404, detail="Predictions not found!")

    return predictions


@router.get("/recommendation", response_model=models.RecommendationModel)
def get_recommendation(month: int, location: str, db: Session = Depends(get_db)): 

    recommendation = query_recommendation(month, location, db)

    if recommendation is None: 
        raise HTTPException(status_code=404, detail="Recommendation not available!")

    return recommendation

