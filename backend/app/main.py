
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.db_models import Event
from app.models import EventResponse


app = FastAPI(
    title="Grandavox API",
    description="Backend services for intelligent live entertainment.",
    version="0.2.0",
)


# FastAPI dependency for a request-scoped database session.
# Each request receives a session that closes afterward.
DatabaseSession = Annotated[Session, Depends(get_db)]


@app.get("/")
def root():
    """Return basic information about the API."""
    return {
        "name": "Grandavox",
        "message": "Welcome to the Grandavox API",
        "version": "0.2.0",
    }


@app.get("/health")
def health_check():
    """
    Confirm the API process is responding.

    This does not check the database connection.
    """
    return {"status": "healthy"}


@app.get("/events", response_model=list[EventResponse])
def get_events(db: DatabaseSession):
    """
    Retrieve all events and their related venues.

    selectinload loads the related venue records while
    the database session is active, avoiding separate
    lazy-loading queries during response serialization.
    """
    statement = (
        select(Event)
        .options(selectinload(Event.venue))
        .order_by(Event.start_time)
    )

    return db.scalars(statement).all()



@app.get(
    "/events/{event_id}",
    response_model=EventResponse,
    responses={
        404: {
            "description": "Event not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Event not found"
                    }
                }
            },
        }
       },
)


def get_event(event_id: int, db: DatabaseSession):
    """
    Retrieve an event by ID, including its venue.

    Return HTTP 404 when the event does not exist.
    """
    statement = (
        select(Event)
        .options(selectinload(Event.venue))
        .where(Event.id == event_id)
    )

    event = db.scalar(statement)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return event
