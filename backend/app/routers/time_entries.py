from __future__ import annotations

from datetime import date as date_cls
from typing import List

from fastapi import APIRouter, HTTPException, Query

from app import store
from app.models import TimeEntryCreate, TimeEntryUpdate, TimeEntryResponse

router = APIRouter(prefix="/time-entries", tags=["time-entries"])


def _error_response(error: str, message: str, detail=None) -> dict:
    return {"error": error, "message": message, "detail": detail}


@router.post("/", response_model=TimeEntryResponse, status_code=201)
async def create_time_entry(payload: TimeEntryCreate) -> TimeEntryResponse:
    entry_dict = store.create_entry(
        date_value=payload.date,
        person_name=payload.person_name,
        team=payload.team,
        activity_description=payload.activity_description,
        start_time=payload.start_time,
        end_time=payload.end_time,
        notes=payload.notes,
    )
    return TimeEntryResponse(**entry_dict)


@router.get("/", response_model=List[TimeEntryResponse])
async def list_time_entries(
    start_date: str | None = Query(default=None, description="Filter start date (YYYY-MM-DD, inclusive)"),
    end_date: str | None = Query(default=None, description="Filter end date (YYYY-MM-DD, inclusive)"),
    person_name: str | None = Query(default=None, description="Filter by person name (case-insensitive exact match)"),
    team: str | None = Query(default=None, description="Filter by team (case-insensitive exact match)"),
) -> List[TimeEntryResponse]:
    start_date_value = None
    end_date_value = None

    try:
        if start_date is not None:
            start_date_value = date_cls.fromisoformat(start_date)
        if end_date is not None:
            end_date_value = date_cls.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=_error_response(
                error="invalid_date",
                message="start_date and end_date must be valid ISO dates (YYYY-MM-DD)",
                detail=None,
            ),
        )

    person_name_value = person_name.strip() if person_name is not None else None
    if person_name_value == "":
        person_name_value = None

    team_value = team.strip() if team is not None else None
    if team_value == "":
        team_value = None

    if any([start_date_value, end_date_value, person_name_value, team_value]):
        entries = store.filter_entries(
            start_date=start_date_value,
            end_date=end_date_value,
            person_name=person_name_value,
            team=team_value,
        )
    else:
        entries = store.list_entries()

    return [TimeEntryResponse(**e) for e in entries]


@router.get("/{entry_id}", response_model=TimeEntryResponse)
async def get_time_entry(entry_id: int) -> TimeEntryResponse:
    entry = store.get_entry(entry_id)
    if not entry:
        raise HTTPException(
            status_code=404,
            detail=_error_response("not_found", "Time entry not found", None),
        )
    return TimeEntryResponse(**entry)


@router.patch("/{entry_id}", response_model=TimeEntryResponse)
async def update_time_entry(entry_id: int, payload: TimeEntryUpdate) -> TimeEntryResponse:
    existing = store.get_entry(entry_id)
    if not existing:
        raise HTTPException(
            status_code=404,
            detail=_error_response("not_found", "Time entry not found", None),
        )

    update_data = payload.model_dump(exclude_unset=True)
    entry = store.update_entry(entry_id, **update_data)
    if not entry:
        raise HTTPException(
            status_code=404,
            detail=_error_response("not_found", "Time entry not found", None),
        )
    return TimeEntryResponse(**entry)


@router.delete("/{entry_id}", status_code=204)
async def delete_time_entry(entry_id: int) -> None:
    deleted = store.delete_entry(entry_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=_error_response("not_found", "Time entry not found", None),
        )
    return None
