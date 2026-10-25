from datetime import datetime

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.db_models import Event, Venue
from app.main import app


@pytest.fixture
def client():
    """
    Create an isolated in-memory database for each test.

    Override the application's database dependency so
    tests never write to our development PostgreSQL data.
    """

    # StaticPool allows the in-memory SQLite database
    # to be shared across TestClient threads.
    test_engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=test_engine)

    # Create predictable records for our automated tests.
    with Session(test_engine) as session:
        venue = Venue(
            name="Grandavox Test Arena",
            city="Charlotte",
            state="NC",
            capacity=15000,
        )

        session.add(venue)

        # Flush sends the venue INSERT to the database
        # and makes its generated ID available.
        session.flush()

        # Create an event associated with our test venue.
        event = Event(
            venue_id=venue.id,
            title="Grandavox Test Concert",
            start_time=datetime(2026, 12, 20, 19, 30),
            category="Music",
            description="A fictional concert for API testing.",
            tickets_available=True,
        )

        session.add(event)
        session.commit()

    # Redirect API requests to our isolated test database.
    def override_get_db():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        # Restore normal database behavior after testing.
        app.dependency_overrides.pop(get_db, None)
        test_engine.dispose()

