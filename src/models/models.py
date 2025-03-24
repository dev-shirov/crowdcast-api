from pydantic import BaseModel, Field


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
    water_sports_score: int
    hiking_score: int
    staycation_score: int
    nightlife_score: int


class RecommendationModel(BaseModel):
    recommendation: str
