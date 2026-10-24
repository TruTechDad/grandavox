
from datetime import datetime, timezone

from sqlalchemy import select

from app.database import SessionLocal
from app.db_models import Event, Venue


def seed_database():
    """
    Populate Grandavox with fictional development data.

    Check for existing sample records so repeated runs
    do not create duplicate venues or events.
    """

    # A transaction commits if everything succeeds.
    # If an error occurs, the transaction rolls back.
    with SessionLocal.begin() as session:

        # Search PostgreSQL for the sample arena.
        venue = session.scalar(
            select(Venue).where(
                Venue.name == "Grandavox Arena"
            )
        )

        if venue is None:
            venue = Venue(
                name="Grandavox Arena",
                city="Charlotte",
                state="NC",
                capacity=20000,
            )

            session.add(venue)

            # Send the INSERT to PostgreSQL so the
            # database generates an ID for our venue.
            session.flush()

        # Avoid inserting the same sample event twice.
        existing_event = session.scalar(
            select(Event).where(
                Event.title == "Grandavox Wrestling Championship",
                Event.venue_id == venue.id,
            )
        )

        if existing_event is None:
            event = Event(
                venue_id=venue.id,
                title="Grandavox Wrestling Championship",
                start_time=datetime(
                    2026, 12, 12, 19, 30,
                    tzinfo=timezone.utc,
                ),
                category="Sports",
                description=(
                    "A fictional professional wrestling "
                    "championship hosted at Grandavox Arena."
                ),
                tickets_available=True,
            )

            session.add(event)

    print("Grandavox sample data seeded successfully!")


if __name__ == "__main__":
    seed_database()
