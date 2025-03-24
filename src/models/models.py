from pydantic import BaseModel


class PredictionsModel(BaseModel):
    id: int
    month: int
    year: int
    days_rained: int
    days_cloudy: int
    days_sunny: int
    tourists: int
