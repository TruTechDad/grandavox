
from datetime import datetime

from app.models import Event


# Temporary in-memory data for our first API milestone.
# We'll replace this with PostgreSQL persistence later.
events = [
    Event(
        id=1,
        title="Queen City Music Festival",
        venue="Grandavox Arena",
        location="Charlotte, NC",
        start_time=datetime(2026, 11, 14, 19, 30),
        category="Concert",
        description="An evening of live music.",
        tickets_available=True,
    ),
    Event(
        id=2,
        title="Carolina Wrestling Championship",
        venue="Grandavox Arena",
        location="Charlotte, NC",
        start_time=datetime(2026, 11, 21, 20, 0),
        category="Sports",
        description="A live professional wrestling event.",
        tickets_available=True,
    ),
    Event(
        id=3,
        title="Broadway Under the Stars",
        venue="Grandavox Theater",
        location="Charlotte, NC",
        start_time=datetime(2026, 12, 5, 19, 0),
        category="Theater",
        description="A special theatrical performance.",
        tickets_available=False,
    ),
]
