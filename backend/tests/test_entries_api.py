from datetime import date

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_entries_returns_seed_data():
    response = client.get("/entries")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_filter_entries_by_date_and_person():
    response = client.get("/entries", params={"date": "2026-04-13", "person": "Samuel Sackey"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["person"] == "Samuel Sackey"


def test_invalid_date_query_returns_400():
    response = client.get("/entries", params={"date": "not-a-date"})
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "invalid_date"


def test_create_entry_success():
    payload = {
        "date": "2026-04-15",
        "person": "Test User",
        "team": "QA",
        "activity": "Manual testing of time tracker UI",
        "duration_minutes": 30,
    }
    response = client.post("/entries", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["person"] == "Test User"
    assert data["duration_minutes"] == 30


def test_create_entry_validation_error():
    payload = {
        "date": "2026-04-15",
        "person": " ",  # invalid blank
        "team": "QA",
        "activity": "Manual testing of time tracker UI",
        "duration_minutes": -5,
    }
    response = client.post("/entries", json=payload)
    # FastAPI/Pydantic will return 422 for body validation errors
    assert response.status_code == 422
