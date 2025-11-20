from datetime import datetime
from typing import Optional
import feedparser

from libs.domain.entities.article import Article
from libs.domain.entities.source import Source
from libs.domain.value_objects.topic_hash import TopicHash
from uuid import UUID


class RSSParser:
    """Service for parsing RSS feeds."""

    @staticmethod
    def parse_feed(url: str) -> list[dict]:
        """Parses an RSS feed and returns a list of entries."""
        parsed = feedparser.parse(url)
        return parsed.entries

    @staticmethod
    def entry_to_article(entry: dict, source_id: UUID) -> Article:
        """Converts an RSS entry to an Article entity."""
        title = entry.title
        link = entry.link
        description = getattr(entry, "summary", None)
        published = getattr(entry, "published", None)

        published_at = None
        if published:
            try:
                published_at = datetime(*entry.published_parsed[:6])
            except Exception:
                pass

        return Article.new(
            title=title,
            link=link,
            source_id=source_id,
            description=description,
            published_at=published_at,
        )

