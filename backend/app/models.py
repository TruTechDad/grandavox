
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VenueResponse(BaseModel):
    """
    Define the public API representation of a venue.

    from_attributes allows Pydantic to read fields
    directly from SQLAlchemy ORM objects.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    state: str
    capacity: int | None


class EventResponse(BaseModel):
    """
    Define the event data returned to API clients.

    The nested venue object provides useful venue
    information without duplicating it in the database.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    start_time: datetime
    category: str
    description: str
    tickets_available: bool

    venue_id: int
    venue: VenueResponse


class EventCreate(BaseModel):
    """
    Validate incoming requests to create an event.

    PostgreSQL generates the unique event ID, so
    the client does not need to provide one.
    """

    venue_id: int = Field(gt=0)

    title: str = Field(
        min_length=1,
        max_length=200,
    )

    start_time: datetime

    category: str = Field(
        min_length=1,
        max_length=80,
    )

    description: str = Field(min_length=1)

    tickets_available: bool = True


