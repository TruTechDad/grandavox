
from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Venue(Base):
    """
    Represents a stadium, theater, or entertainment venue.

    One venue can host multiple events.
    """

    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    capacity: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    # Connect the venue to its scheduled events.
    events: Mapped[list["Event"]] = relationship(
        back_populates="venue",
    )


class Event(Base):
    """
    Represents a scheduled live entertainment event.

    Each event belongs to one venue.
    """

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)

    venue_id: Mapped[int] = mapped_column(
        ForeignKey("venues.id"),
        index=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    start_time: Mapped[datetime]

    category: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    tickets_available: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    # Connect the event back to its hosting venue.
    venue: Mapped["Venue"] = relationship(
        back_populates="events",
    )
