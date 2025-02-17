"""
Module for creating and managing the database connection.
"""

from pathlib import Path

from sqlalchemy import exc
from sqlmodel import Session, SQLModel, create_engine


def get_engine():
    """Create and return the database engine."""

    echo = True
    database_path = Path("app/backend/database/data/database.db")

    database_url = f"sqlite:///{database_path}"

    # set the connect args, to disable the check for the same thread:
    connect_args = {"check_same_thread": False}

    engine = create_engine(database_url, echo=echo, connect_args=connect_args)

    # Enable WAL mode for SQLite
    # with engine.connect() as connection:
    #     connection.execute(text("PRAGMA journal_mode=WAL;"))

    return engine


def initialize_database():
    """Create the database tables if they don't exist."""
    engine = get_engine()
    try:
        SQLModel.metadata.create_all(engine)

    except exc.SQLAlchemyError as e:
        print(f"An error occurred while creating the database tables: {e}")
        raise exc.OperationalError(
            "An error occurred while creating the database tables."
        )
    except exc.OperationalError as e:
        print(f"An error occurred while creating the database tables: {e}")
        raise exc.OperationalError(
            "An error occurred while creating the database tables."
        )


def get_session():
    with Session(get_engine()) as session:
        yield session
