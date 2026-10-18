
from datetime import datetime

from pydantic import BaseModel, Field


class Event(BaseModel):
    """
    Define the data contract for an entertainment event.

    FastAPI uses this model to validate and serialize
    event data returned to API clients.
    """

    id: int
    title: str = Field(min_length=1)
    venue: str = Field(min_length=1)
    location: str
    start_time: datetime
    category: str
    description: str
    tickets_available: bool = True
