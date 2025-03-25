from pydantic import BaseModel, Field
from typing import Dict


class RecommendationRequest(BaseModel):
    month: int = Field(description="Month selected")
    location: str = Field(description="Location selected")
    activity: str = Field(description="Selected activity")


class PredictionsModel(BaseModel):
    id: int
    location: str
    month: int
    days_rained: int
    days_cloudy: int
    days_sunny: int
    tourists: int
    crowded: str
    water_sports_score: str
    hiking_score: str
    staycation_score: str
    nightlife_score: str


class RecommendationModel(BaseModel):
    Recommended: list[str]
    NonRecommended: list[str]
    Recommendation: list[str]
