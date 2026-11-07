
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Find the Grandavox repository root.
# Our .env file lives beside compose.yaml.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


# Read connection settings from the environment
# instead of hardcoding database credentials.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing from the environment."
    )


# SQLAlchemy manages PostgreSQL connections
# through this engine.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# Each database session represents a unit of work.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for our database table models."""
    pass


def get_db():
    """Provide and close a database session."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def test_connection():
    """Verify that SQLAlchemy can query PostgreSQL."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar_one()


if __name__ == "__main__":
    print("Database connection test:", test_connection())
