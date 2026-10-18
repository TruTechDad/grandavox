
from fastapi.testclient import TestClient

from app.main import app


# TestClient lets us exercise API routes without
# starting a separate development server.
client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_all_events():
    response = client.get("/events")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_event_by_id():
    response = client.get("/events/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Queen City Music Festival"


def test_get_missing_event():
    response = client.get("/events/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"
