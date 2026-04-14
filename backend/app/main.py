from datetime import date as date_cls

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app import store
from app.models import TimeEntryCreate, TimeEntryResponse

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


@app.post("/entries", response_model=TimeEntryResponse, status_code=201)
async def create_time_entry(payload: TimeEntryCreate) -> TimeEntryResponse:
    entry_dict = store.create_entry(
        date_value=payload.date,
        person=payload.person,
        team=payload.team,
        activity=payload.activity,
        duration_minutes=payload.duration_minutes,
    )
    return TimeEntryResponse(**entry_dict)


@app.get("/entries", response_model=list[TimeEntryResponse])
async def list_time_entries(
    date: str | None = Query(default=None, description="Filter by date (YYYY-MM-DD)"),
    person: str | None = Query(default=None, description="Filter by person (exact match, case-insensitive)"),
):
    date_value = None
    if date is not None:
        try:
            date_value = date_cls.fromisoformat(date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "invalid_date",
                    "message": "date must be a valid ISO date (YYYY-MM-DD)",
                    "detail": None,
                },
            )

    person_value = person.strip() if person is not None else None
    if person_value == "":
        person_value = None

    entries = store.list_entries(date_value=date_value, person=person_value)
    return [TimeEntryResponse(**e) for e in entries]
