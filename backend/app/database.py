import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

# Load variables from .env into the environment
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# The engine manages the actual connection pool to Postgres.
# echo=True logs every SQL statement Claude — sorry, SQLModel — runs, which is
# great for learning (you'll see the raw SQL) but you'd turn this off in production.
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """
    Creates all tables based on our SQLModel classes.
    NOTE: We'll only use this for a quick first run. Once we introduce Alembic,
    migrations will take over this responsibility — this function is a
    beginner-friendly stepping stone, not a long-term migration strategy.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    This is a 'dependency' function. FastAPI will call this for us on every
    request that needs a DB session, hand the session to our endpoint function,
    and automatically close it afterward — even if an error occurs.

    We'll plug this into endpoints using FastAPI's `Depends()` shortly.
    """
    with Session(engine) as session:
        yield session