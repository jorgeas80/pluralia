from unittest.mock import AsyncMock, Mock

import pytest

from libs.domain.services.embedding_service import EmbeddingService
from services.ingest.src.application.ingest_news import IngestNews
from services.ingest.src.infrastructure.services.rss_parser import UndatedArticleError
from tests.factories.source_factory import SourceFactory


@pytest.mark.asyncio
async def test_ingest_skips_rss_entries_without_publication_dates():
    source = SourceFactory.build()
    source_repository = Mock(find_by_name=AsyncMock(return_value=source))
    article_repository = Mock(find_by_link=AsyncMock())
    news_group_repository = Mock()
    rss_parser = Mock(
        parse_feed=Mock(return_value=[{"title": "Undated story"}]),
        entry_to_article=Mock(side_effect=UndatedArticleError("missing date")),
    )
    embedding_service = Mock(spec=EmbeddingService)

    ingest = IngestNews(
        source_repository=source_repository,
        article_repository=article_repository,
        news_group_repository=news_group_repository,
        rss_parser=rss_parser,
        embedding_service=embedding_service,
    )

    await ingest.execute("Example", "https://example.com/feed", source.bias)

    article_repository.find_by_link.assert_not_awaited()
    embedding_service.generate_embedding.assert_not_called()
