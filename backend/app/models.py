from __future__ import annotations

from datetime import date as date_type
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TimeEntryBase(BaseModel):
    date: date_type = Field(..., description="Entry date (YYYY-MM-DD)")
    person: str = Field(..., min_length=1, description="Person who logged the time")
    team: str = Field(..., min_length=1, description="Team name")
    activity: str = Field(..., min_length=1, description="Description of the activity")
    duration_minutes: int = Field(..., gt=0, description="Duration in minutes (must be positive)")

    @field_validator("person", "team", "activity")
    @classmethod
    def non_empty_trimmed(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v.strip()


class TimeEntryCreate(TimeEntryBase):
    pass


class TimeEntryResponse(TimeEntryBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True


class EntriesQueryParams(BaseModel):
    date: Optional[date_type] = None
    person: Optional[str] = None

    @field_validator("person")
    @classmethod
    def normalize_person(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        return v or None
