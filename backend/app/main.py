from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import store  # noqa: F401  # ensure store is imported so seed data is ready

app = FastAPI(title="Team Time Activity Tracker API")

# CORS configuration - allow all origins for internal MVP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    """Healthcheck endpoint required by Railway."""
    return {"status": "ok"}
