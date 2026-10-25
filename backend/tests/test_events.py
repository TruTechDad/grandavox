
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

