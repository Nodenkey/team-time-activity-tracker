from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time, datetime
from typing import List, Optional, Dict, Any


@dataclass
class TimeEntry:
    id: int
    date: date
    person_name: str
    team: str
    activity_description: str
    start_time: time
    end_time: time
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None


_entries: Dict[int, TimeEntry] = {}
_next_id: int = 1


def _seed_data() -> None:
    global _entries, _next_id
    if _entries:
        return

    seed_items = [
        TimeEntry(
            id=1,
            date=date(2026, 4, 13),
            person_name="Samuel Sackey",
            team="MCP Testing Team",
            activity_description="Implemented HTML form for time tracking demo",
            start_time=time(9, 0),
            end_time=time(10, 30),
            notes="Initial prototype for internal review",
            created_at=datetime(2026, 4, 13, 9, 0, 0),
        ),
        TimeEntry(
            id=2,
            date=date(2026, 4, 13),
            person_name="Ato Toffah",
            team="MCP Testing Team",
            activity_description="Designed FastAPI backend for time tracker MVP",
            start_time=time(10, 30),
            end_time=time(12, 30),
            notes="Covered CRUD, filters, and in-memory store design",
            created_at=datetime(2026, 4, 13, 10, 30, 0),
        ),
        TimeEntry(
            id=3,
            date=date(2026, 4, 14),
            person_name="Sara Gordic",
            team="MCP Testing Team",
            activity_description="Documented API contract and usage examples",
            start_time=time(11, 15),
            end_time=time(12, 15),
            notes="Prepared handoff for frontend integration",
            created_at=datetime(2026, 4, 14, 11, 15, 0),
        ),
    ]

    for item in seed_items:
        _entries[item.id] = item

    _next_id = max(_entries.keys()) + 1


_seed_data()


def serialize_entry(entry: TimeEntry) -> Dict[str, Any]:
    return {
        "id": entry.id,
        "date": entry.date.isoformat(),
        "person_name": entry.person_name,
        "team": entry.team,
        "activity_description": entry.activity_description,
        "start_time": entry.start_time.isoformat(timespec="minutes"),
        "end_time": entry.end_time.isoformat(timespec="minutes"),
        "notes": entry.notes,
        "created_at": entry.created_at.isoformat(),
        "updated_at": entry.updated_at.isoformat() if entry.updated_at else None,
    }


def create_entry(
    *,
    date_value: date,
    person_name: str,
    team: str,
    activity_description: str,
    start_time: time,
    end_time: time,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    global _next_id

    entry = TimeEntry(
        id=_next_id,
        date=date_value,
        person_name=person_name,
        team=team,
        activity_description=activity_description,
        start_time=start_time,
        end_time=end_time,
        notes=notes,
        created_at=datetime.utcnow(),
    )
    _entries[_next_id] = entry
    _next_id += 1
    return serialize_entry(entry)


def list_entries() -> List[Dict[str, Any]]:
    return [serialize_entry(e) for e in sorted(_entries.values(), key=lambda e: e.created_at, reverse=True)]


def filter_entries(
    *,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    person_name: Optional[str] = None,
    team: Optional[str] = None,
) -> List[Dict[str, Any]]:
    def matches(entry: TimeEntry) -> bool:
        if start_date and entry.date < start_date:
            return False
        if end_date and entry.date > end_date:
            return False
        if person_name and entry.person_name.lower() != person_name.lower():
            return False
        if team and entry.team.lower() != team.lower():
            return False
        return True

    filtered = [e for e in _entries.values() if matches(e)]
    filtered.sort(key=lambda e: e.created_at, reverse=True)
    return [serialize_entry(e) for e in filtered]


def get_entry(entry_id: int) -> Optional[Dict[str, Any]]:
    entry = _entries.get(entry_id)
    if not entry:
        return None
    return serialize_entry(entry)


def update_entry(entry_id: int, **fields: Any) -> Optional[Dict[str, Any]]:
    entry = _entries.get(entry_id)
    if not entry:
        return None

    for key, value in fields.items():
        if value is None:
            continue
        if hasattr(entry, key):
            setattr(entry, key, value)

    entry.updated_at = datetime.utcnow()
    return serialize_entry(entry)


def delete_entry(entry_id: int) -> bool:
    if entry_id not in _entries:
        return False
    del _entries[entry_id]
    return True
