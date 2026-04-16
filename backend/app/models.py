from __future__ import annotations

from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class TimeEntryBase(BaseModel):
    date: date = Field(..., description="Entry date (YYYY-MM-DD)")
    person_name: str = Field(..., min_length=1, description="Person who logged the time")
    team: str = Field(..., min_length=1, description="Team or department name")
    activity_description: str = Field(..., min_length=1, description="Description of the activity")
    start_time: time = Field(..., description="Start time of the activity (HH:MM)")
    end_time: time = Field(..., description="End time of the activity (HH:MM), must be after start_time")
    notes: Optional[str] = Field(default=None, description="Optional notes for the entry")

    @field_validator("person_name", "team", "activity_description")
    @classmethod
    def non_empty_trimmed(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v.strip()

    @field_validator("notes")
    @classmethod
    def normalize_notes(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        return v or None

    @model_validator(mode="after")
    def validate_time_range(self) -> "TimeEntryBase":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class TimeEntryCreate(TimeEntryBase):
    """Payload for creating a new time entry."""


class TimeEntryUpdate(BaseModel):
    date: Optional[date] = Field(default=None, description="Updated entry date")
    person_name: Optional[str] = Field(default=None, description="Updated person name")
    team: Optional[str] = Field(default=None, description="Updated team name")
    activity_description: Optional[str] = Field(default=None, description="Updated activity description")
    start_time: Optional[time] = Field(default=None, description="Updated start time")
    end_time: Optional[time] = Field(default=None, description="Updated end time")
    notes: Optional[str] = Field(default=None, description="Updated notes")

    @field_validator("person_name", "team", "activity_description")
    @classmethod
    def non_empty_trimmed_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("must not be empty when provided")
        return v

    @field_validator("notes")
    @classmethod
    def normalize_notes_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        return v or None

    @model_validator(mode="after")
    def validate_time_range(self) -> "TimeEntryUpdate":
        if self.start_time is not None and self.end_time is not None:
            if self.end_time <= self.start_time:
                raise ValueError("end_time must be after start_time when both are provided")
        return self


class TimeEntryResponse(TimeEntryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EntriesQueryParams(BaseModel):
    start_date: Optional[date] = Field(default=None, description="Filter start date (inclusive)")
    end_date: Optional[date] = Field(default=None, description="Filter end date (inclusive)")
    person_name: Optional[str] = Field(default=None, description="Filter by person name (case-insensitive exact match)")
    team: Optional[str] = Field(default=None, description="Filter by team (case-insensitive exact match)")

    @field_validator("person_name", "team")
    @classmethod
    def normalize_str_filters(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        return v or None

    @model_validator(mode="after")
    def validate_date_range(self) -> "EntriesQueryParams":
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self
