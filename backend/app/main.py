
from fastapi import FastAPI, HTTPException

from app.data import events
from app.models import Event


# Create the FastAPI application instance.
app = FastAPI(
    title="Grandavox API",
    description="Backend services for intelligent live entertainment.",
    version="0.1.0",
)


@app.get("/")
def root():
    """Return basic information about the API."""
    return {
        "name": "Grandavox",
        "message": "Welcome to the Grandavox API",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    """Confirm the application can respond to requests."""
    return {"status": "healthy"}


@app.get("/events", response_model=list[Event])
def get_events():
    """Retrieve all available event records."""
    return events


@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int):
    """
    Retrieve a single event by ID.

    Return HTTP 404 when the requested event
    does not exist in our collection.
    """
    for event in events:
        if event.id == event_id:
            return event

    raise HTTPException(
        status_code=404,
        detail="Event not found",
    )
