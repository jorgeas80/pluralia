"""Application layer test fixtures."""
import pytest
from unittest.mock import AsyncMock
from libs.domain.repositories.article_repository import ArticleRepository
from libs.domain.repositories.source_repository import SourceRepository


@pytest.fixture
def mock_article_repository():
    """Mock ArticleRepository."""
    return AsyncMock(spec=ArticleRepository)


@pytest.fixture
def mock_source_repository():
    """Mock SourceRepository."""
    return AsyncMock(spec=SourceRepository)

