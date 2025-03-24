from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = Field("sqlite:///./src/data/predictions.db")
    GEMINI_API_KEY: str = Field("")
    GEMINI_URL: str = Field("")


settings = Settings()
