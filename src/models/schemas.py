from typing import Dict

from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session

from .database import Base



class Predictions(Base):
    """tickets table definition"""

    __tablename__ = "boracay_predictions"

    id = Column(Integer, primary_key=True)
    month = Column(Integer)
    year = Column(Integer)
    days_rained = Column(Integer)
    days_cloudy = Column(Integer)
    days_sunny = Column(Integer)
    tourists = Column(Integer)


def query_predictions(db: Session) -> Dict[str, list[Predictions]]:
    return {"predictions": db.query(Predictions).all()}
