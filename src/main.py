from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.v1 import predictions
from src.models.database import Base, engine

# create tickets db
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crowd Cast API",
    description="Rest api for getting Crowd Cast Predictions and LLM.",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",  # swagger UI
    redoc_url="/redoc",
)  # ReDoc
app.include_router(predictions.router)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def root_ping():
    """
    Server liveness check.
    """
    return {"status": "ok", "message": "I'm up!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
