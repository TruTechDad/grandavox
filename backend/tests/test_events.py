
from fastapi.testclient import TestClient

from app.main import app


# TestClient lets us exercise API routes without
# starting a separate development server.
client = TestClient(app)



def test_health_check(client):
    """The health endpoint should respond successfully."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_events(client):
    """The events endpoint should return our test data."""
    response = client.get("/events")

    assert response.status_code == 200

    events = response.json()

    assert len(events) == 1
    assert events[0]["title"] == "Grandavox Test Concert"
    assert events[0]["venue"]["name"] == "Grandavox Test Arena"


def test_get_event_by_id(client):
    """An existing event should return HTTP 200."""
    response = client.get("/events/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Grandavox Test Concert"


def test_get_missing_event(client):
    """A nonexistent event should return HTTP 404."""
    response = client.get("/events/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"



def test_create_event(client):
    """A valid request creates an event and returns HTTP 201."""
    event_data = {
        "venue_id": 1,
        "title": "Grandavox Comedy Night",
        "start_time": "2026-12-22T20:00:00",
        "category": "Comedy",
        "description": "A fictional comedy performance.",
        "tickets_available": True,
    }

    response = client.post("/events", json=event_data)

    assert response.status_code == 201

    created_event = response.json()

    assert created_event["title"] == "Grandavox Comedy Night"
    assert created_event["venue"]["name"] == "Grandavox Test Arena"
    assert created_event["id"] > 0

    # Confirm the record can also be retrieved.
    get_response = client.get(
        f"/events/{created_event['id']}"
    )
    assert get_response.status_code == 200


def test_create_event_with_missing_venue(client):
    """Reject events associated with nonexistent venues."""
    event_data = {
        "venue_id": 999,
        "title": "Unknown Venue Event",
        "start_time": "2026-12-22T20:00:00",
        "category": "Music",
        "description": "An event with an invalid venue.",
    }

    response = client.post("/events", json=event_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Venue not found"


def test_create_event_with_invalid_data(client):
    """Reject event requests containing invalid fields."""
    event_data = {
        "venue_id": -1,
        "title": "",
        "start_time": "not-a-date",
        "category": "",
        "description": "",
    }

    response = client.post("/events", json=event_data)

    assert response.status_code == 422
