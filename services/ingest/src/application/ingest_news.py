from typing import Optional
from uuid import UUID

from libs.domain.entities.article import Article
from libs.domain.entities.news_group import NewsGroup
from libs.domain.entities.source import Source
from libs.domain.repositories.article_repository import ArticleRepository
from libs.domain.repositories.news_group_repository import NewsGroupRepository
from libs.domain.repositories.source_repository import SourceRepository
from libs.domain.value_objects.bias import Bias
from libs.domain.value_objects.topic_hash import TopicHash
from services.ingest.src.infrastructure.services.rss_parser import RSSParser


class IngestNews:
    """Use case for ingesting news from RSS feeds."""

    def __init__(
        self,
        source_repository: SourceRepository,
        article_repository: ArticleRepository,
        news_group_repository: NewsGroupRepository,
        rss_parser: RSSParser,
    ):
        self._source_repository = source_repository
        self._article_repository = article_repository
        self._news_group_repository = news_group_repository
        self._rss_parser = rss_parser

    async def execute(
        self,
        source_name: str,
        source_url: str,
        bias: Bias,
        limit: int = 10,
    ) -> None:
        """Ingests news from a source RSS feed."""
        source = await self._ensure_source_exists(source_name, source_url, bias)

        entries = self._rss_parser.parse_feed(source_url)

        for entry in entries[:limit]:
            article = self._rss_parser.entry_to_article(entry, source.id)

            existing_article = await self._article_repository.find_by_link(article.link)
            if existing_article:
                continue

            topic_hash = TopicHash.from_title(article.title)
            group = await self._ensure_group_exists(topic_hash)

            article_with_group = article.assign_to_group(group.id)
            await self._article_repository.save(article_with_group)

    async def _ensure_source_exists(self, name: str, url: Optional[str], bias: Bias) -> Source:
        """Ensures a source exists, creating it if necessary."""
        source = await self._source_repository.find_by_name(name)
        if not source:
            source = Source.new(name=name, url=url, bias=bias)
            await self._source_repository.save(source)
            source = await self._source_repository.find_by_name(name)
        return source

    async def _ensure_group_exists(self, topic_hash: TopicHash) -> NewsGroup:
        """Ensures a news group exists, creating it if necessary."""
        group = await self._news_group_repository.find_by_topic_hash(topic_hash)
        if not group:
            group = NewsGroup.new(topic_hash=topic_hash)
            await self._news_group_repository.save(group)
            group = await self._news_group_repository.find_by_topic_hash(topic_hash)
        return group

