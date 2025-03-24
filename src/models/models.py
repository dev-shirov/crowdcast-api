from pydantic import BaseModel, Field
import uuid 


class GenerateVacationRecommendationResponse(BaseModel): 

    id: uuid.UUID = Field(description="ID of the generated recommendation")
    completed: bool = Field(
        description="Flag indicating if the generation was completed"
    )

class GetVacationRecommendationResponse(GenerateVacationRecommendationResponse):
    idea: str = Field(description="The generated idea")

class GenerateVacationRecommendationRequest(BaseModel):
    month: str = Field(description="Month selected")
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


class RecommendationModel(GenerateVacationRecommendationResponse):
    recommendation: str
