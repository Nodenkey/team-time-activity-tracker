from datetime import date

from app import store


def test_seed_data_present():
    entries = store.list_entries()
    assert len(entries) >= 3


def test_create_entry_increments_count():
    before = len(store.list_entries())
    store.create_entry(
        date_value=date(2026, 4, 15),
        person="Test User",
        team="QA",
        activity="Wrote tests for time tracker backend",
        duration_minutes=45,
    )
    after = len(store.list_entries())
    assert after == before + 1


def test_filter_by_date_and_person():
    # Use a known seeded entry
    entries = store.list_entries(date_value=date(2026, 4, 13), person="Samuel Sackey")
    assert len(entries) == 1
    assert entries[0]["person"] == "Samuel Sackey"
