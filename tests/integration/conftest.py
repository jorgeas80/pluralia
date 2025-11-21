"""Integration test fixtures."""
import pytest
import os
from sqlmodel import SQLModel, create_engine, Session
from services.api.src.infrastructure.database.db import get_session
from services.api.src.infrastructure.database.models import SourceModel, ArticleModel, NewsGroupModel


@pytest.fixture(scope="function")
def test_database_url():
    """Test database URL."""
    return os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pluralia_test")


@pytest.fixture(scope="function")
def test_engine(test_database_url):
    """Test database engine."""
    engine = create_engine(test_database_url, echo=False)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Test database session."""
    with Session(test_engine) as session:
        yield session
        session.rollback()

