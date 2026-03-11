import os
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager

from services.api.src.infrastructure.database.models import SourceModel, ArticleModel, NewsGroupModel

DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pluralia")
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    """Initialize database tables. Drops existing tables first in development."""
    # Only drop tables in development (when DROP_DB=true)
    drop_db = os.getenv("DROP_DB", "false").lower() == "true"
    if drop_db:
        SQLModel.metadata.drop_all(engine)
        # Create tables with correct types (for initial setup)
        SQLModel.metadata.create_all(engine)
    # Otherwise, migrations should be run manually with: alembic upgrade head


@contextmanager
def get_session():
    """Get a database session context manager."""
    with Session(engine) as session:
        yield session

