
from datetime import datetime

from pydantic import BaseModel, ConfigDict


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

