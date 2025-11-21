"""Tests for GetNews use case."""
import pytest
from unittest.mock import AsyncMock
from services.api.src.application.get_news import GetNews
from tests.factories.source_factory import SourceFactory
from tests.factories.article_factory import ArticleFactory
from libs.domain.value_objects.bias import Bias


async def test_execute_returns_news_from_all_sources(mock_article_repository, mock_source_repository):
    source1 = SourceFactory.build(name="El País", bias=Bias.left())
    source2 = SourceFactory.build(name="ABC", bias=Bias.right())
    
    article1 = ArticleFactory.build(title="News 1", source_id=source1.id)
    article2 = ArticleFactory.build(title="News 2", source_id=source2.id)
    
    mock_source_repository.find_all = AsyncMock(return_value=[source1, source2])
    mock_article_repository.find_by_source_id = AsyncMock(side_effect=[[article1], [article2]])
    
    use_case = GetNews(
        article_repository=mock_article_repository,
        source_repository=mock_source_repository,
    )
    
    result = await use_case.execute(limit=10)
    
    assert len(result) == 2
    assert result[0]["title"] == "News 1"
    assert result[0]["source"] == "El País"
    assert result[0]["bias"] == "left"
    assert result[1]["title"] == "News 2"
    assert result[1]["source"] == "ABC"
    assert result[1]["bias"] == "right"
    mock_source_repository.find_all.assert_awaited_once()
    assert mock_article_repository.find_by_source_id.await_count == 2


async def test_execute_respects_limit_parameter(mock_article_repository, mock_source_repository):
    source = SourceFactory.build()
    all_articles = [ArticleFactory.build(source_id=source.id) for _ in range(5)]
    limited_articles = all_articles[:3]
    
    mock_source_repository.find_all = AsyncMock(return_value=[source])
    mock_article_repository.find_by_source_id = AsyncMock(return_value=limited_articles)
    
    use_case = GetNews(
        article_repository=mock_article_repository,
        source_repository=mock_source_repository,
    )
    
    result = await use_case.execute(limit=3)
    
    mock_article_repository.find_by_source_id.assert_awaited_once_with(source.id, limit=3)
    assert len(result) == 3


async def test_execute_handles_empty_sources(mock_article_repository, mock_source_repository):
    mock_source_repository.find_all = AsyncMock(return_value=[])
    
    use_case = GetNews(
        article_repository=mock_article_repository,
        source_repository=mock_source_repository,
    )
    
    result = await use_case.execute()
    
    assert result == []
    mock_article_repository.find_by_source_id.assert_not_awaited()


async def test_execute_handles_articles_without_published_at(mock_article_repository, mock_source_repository):
    source = SourceFactory.build()
    article = ArticleFactory.build(source_id=source.id, published_at=None)
    
    mock_source_repository.find_all = AsyncMock(return_value=[source])
    mock_article_repository.find_by_source_id = AsyncMock(return_value=[article])
    
    use_case = GetNews(
        article_repository=mock_article_repository,
        source_repository=mock_source_repository,
    )
    
    result = await use_case.execute()
    
    assert len(result) == 1
    assert result[0]["published"] is None

