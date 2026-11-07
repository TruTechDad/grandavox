
from app.database import Base, engine

# Import ORM models so SQLAlchemy registers
# both tables before creating the schema.
from app import db_models  # noqa: F401


def create_tables():
    """
    Create missing database tables.

    This is an initial development setup.
    Later, Alembic migrations will manage
    schema changes safely.
    """
    Base.metadata.create_all(bind=engine)

    print("Grandavox database tables created successfully!")


if __name__ == "__main__":
    create_tables()
