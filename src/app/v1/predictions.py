from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Optional

from src.models import models
from src.models.database import get_db
from src.models.schemas import query_recommendation, query_predictions


router = APIRouter()


@router.get("/predictions", response_model=Dict[str, list[models.PredictionsModel]])
def get_predictions(
    month: Optional[int] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db),
):
    predictions = query_predictions(month, location, db)

    if predictions is None:
        raise HTTPException(status_code=404, detail="Predictions not found!")

    return predictions


@router.post("/recommendation", response_model=models.RecommendationModel)
def get_recommendation(
    input: models.RecommendationRequest, db: Session = Depends(get_db)
):
    input_dict = input.model_dump()
    month = input_dict["month"]
    location = input_dict["location"]
    activity = input_dict["activity"]

    recommendation = query_recommendation(month, location, activity, db)

    if recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not available!")

    return recommendation
