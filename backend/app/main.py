
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.db_models import Event, Venue
from app.models import EventCreate, EventResponse




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


@app.post(
    "/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"description": "Venue not found"},
    },
)
def create_event(event_data: EventCreate, db: DatabaseSession):
    """
    Create a new entertainment event in PostgreSQL.

    The event must reference an existing venue.
    """

    # Verify the selected venue exists before inserting.
    venue = db.get(Venue, event_data.venue_id)

    if venue is None:
        raise HTTPException(
            status_code=404,
            detail="Venue not found",
        )

    # Transform validated request data into a database entity.
    new_event = Event(**event_data.model_dump())

    db.add(new_event)

    try:
        # Save the new event and generate its database ID.
        db.commit()
    except Exception:
        db.rollback()
        raise

    # Reload database-generated values.
    db.refresh(new_event)

    # Attach venue information for response serialization.
    new_event.venue = venue

    return new_event
