from typing import Optional, Dict

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from .database import Base

from .models import RecommendationModel

from src.chains.crowdcast_recommendation import generate_vacation_idea_chain


class Predictions(Base):
    """tickets table definition"""

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    location = Column(String)
    month = Column(Integer)
    days_rained = Column(Integer)
    days_cloudy = Column(Integer)
    days_sunny = Column(Integer)
    tourists = Column(Integer)
    crowded = Column(String)
    water_sports_score = Column(Integer)
    hiking_score = Column(Integer)
    staycation_score = Column(Integer)
    nightlife_score = Column(Integer)


def query_predictions(
    month: Optional[int], location: Optional[str], db: Session
) -> Dict[str, list[Predictions]]:
    if location and month:
        return {
            "predictions": db.query(Predictions)
            .filter(Predictions.location == location, Predictions.month == month)
            .all()
        }
    elif location is None and month:
        return {
            "predictions": db.query(Predictions)
            .filter(Predictions.month == month)
            .all()
        }
    elif location and month is None:
        return {
            "predictions": db.query(Predictions)
            .filter(Predictions.location == location)
            .all()
        }
    else:
        return {"predictions": db.query(Predictions).all()}


def query_recommendation(
    month: int, location: str, activity: str, db: Session
) -> Optional[RecommendationModel]:
    input_dict = query_predictions(month, location, db)["predictions"][0].__dict__

    month = input_dict["month"]
    location = input_dict["location"]
    days_rained = input_dict["days_rained"]
    days_cloudy = input_dict["days_cloudy"]
    days_sunny = input_dict["days_sunny"]
    crowded = "High" if input_dict["crowded"] else "Low"

    recommendation_str = generate_vacation_idea_chain(
        month, location, days_rained, days_cloudy, days_sunny, crowded, activity
    )

    return RecommendationModel(recommendation=recommendation_str)
