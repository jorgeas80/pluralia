from typing import Optional
from uuid import UUID

from libs.domain.entities.article import Article
from libs.domain.entities.news_group import NewsGroup
from libs.domain.entities.source import Source
from libs.domain.repositories.article_repository import ArticleRepository
from libs.domain.repositories.news_group_repository import NewsGroupRepository
from libs.domain.repositories.source_repository import SourceRepository
from libs.domain.services.embedding_service import EmbeddingService
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
        embedding_service: EmbeddingService,
        similarity_threshold: float = 0.7,
    ):
        self._source_repository = source_repository
        self._article_repository = article_repository
        self._news_group_repository = news_group_repository
        self._rss_parser = rss_parser
        self._embedding_service = embedding_service
        self._similarity_threshold = similarity_threshold

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

            # Generate embedding for the article title
            article_embedding = self._embedding_service.generate_embedding(article.title)
            
            # Try to find a similar group using embeddings
            group = await self._find_or_create_group_by_similarity(article.title, article_embedding)

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

    async def _find_or_create_group_by_similarity(self, title: str, embedding: list[float]) -> NewsGroup:
        """Finds a similar group by embedding similarity, or creates a new one."""
        # Get all existing groups
        existing_groups = await self._news_group_repository.find_all()
        
        # Find the most similar group
        best_match = None
        best_similarity = 0.0
        
        for group in existing_groups:
            if group.embedding is not None:
                similarity = self._embedding_service.calculate_similarity(embedding, group.embedding)
                if similarity > best_similarity and similarity >= self._similarity_threshold:
                    best_similarity = similarity
                    best_match = group
        
        # If we found a similar group, return it
        if best_match:
            return best_match
        
        # Otherwise, create a new group with the embedding
        topic_hash = TopicHash.from_title(title)
        new_group = NewsGroup.new(topic_hash=topic_hash, embedding=embedding)
        await self._news_group_repository.save(new_group)
        
        # Reload to get the persisted group
        saved_group = await self._news_group_repository.find_by_topic_hash(topic_hash)
        return saved_group if saved_group else new_group

