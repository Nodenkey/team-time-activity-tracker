from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime
from typing import List, Optional


@dataclass
class TimeEntry:
    id: int
    date: date
    person: str
    team: str
    activity: str
    duration_minutes: int
    created_at: datetime


# In-memory store for time entries
_entries: List[TimeEntry] = []
_next_id: int = 1


def _seed_data() -> None:
    global _entries, _next_id
    if _entries:
        return

    seed_items = [
        TimeEntry(
            id=1,
            date=date(2026, 4, 13),
            person="Samuel Sackey",
            team="MCP Testing Team",
            activity="Implemented HTML form for time tracking demo",
            duration_minutes=90,
            created_at=datetime(2026, 4, 13, 9, 0, 0),
        ),
        TimeEntry(
            id=2,
            date=date(2026, 4, 13),
            person="Ato Toffah",
            team="MCP Testing Team",
            activity="Designed FastAPI backend for time tracker MVP",
            duration_minutes=120,
            created_at=datetime(2026, 4, 13, 10, 30, 0),
        ),
        TimeEntry(
            id=3,
            date=date(2026, 4, 14),
            person="Sara Gordic",
            team="MCP Testing Team",
            activity="Documented API contract and usage examples",
            duration_minutes=60,
            created_at=datetime(2026, 4, 14, 11, 15, 0),
        ),
    ]

    _entries.extend(seed_items)
    _next_id = len(_entries) + 1


_seed_data()


def create_entry(*, date_value: date, person: str, team: str, activity: str, duration_minutes: int) -> dict:
    """Create a new time entry and return it as a dict."""
    global _next_id

    entry = TimeEntry(
        id=_next_id,
        date=date_value,
        person=person,
        team=team,
        activity=activity,
        duration_minutes=duration_minutes,
        created_at=datetime.utcnow(),
    )
    _entries.append(entry)
    _next_id += 1
    return serialize_entry(entry)


def list_entries(*, date_value: Optional[date] = None, person: Optional[str] = None) -> List[dict]:
    """Return all entries, optionally filtered by date and/or person (case-insensitive)."""

    def matches(entry: TimeEntry) -> bool:
        if date_value is not None and entry.date != date_value:
            return False
        if person is not None and entry.person.lower() != person.lower():
            return False
        return True

    return [serialize_entry(e) for e in _entries if matches(e)]


def serialize_entry(entry: TimeEntry) -> dict:
    data = asdict(entry)
    data["date"] = entry.date.isoformat()
    data["created_at"] = entry.created_at.isoformat()
    return data
