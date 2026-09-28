from datetime import datetime, timezone
from typing import Optional
import feedparser

from libs.domain.entities.article import Article
from uuid import UUID


class UndatedArticleError(ValueError):
    """Raised when an RSS entry has no usable publication timestamp."""


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
        if isinstance(entry, dict):
            # FeedParserDict aliases a missing published_parsed to updated_parsed
            # with a deprecation warning; read its stored keys directly instead.
            published_parsed = dict.get(entry, "published_parsed")
            updated_parsed = dict.get(entry, "updated_parsed")
        else:
            published_parsed = getattr(entry, "published_parsed", None)
            updated_parsed = getattr(entry, "updated_parsed", None)
        published_parsed = published_parsed or updated_parsed
        if not published_parsed:
            raise UndatedArticleError(f"RSS entry has no valid publication date: {link}")
        try:
            # feedparser has already converted the source offset to UTC.
            published_at = datetime(*published_parsed[:6], tzinfo=timezone.utc)
        except (TypeError, ValueError, IndexError) as error:
            raise UndatedArticleError(
                f"RSS entry has no valid publication date: {link}"
            ) from error

        return Article.new(
            title=title,
            link=link,
            source_id=source_id,
            description=description,
            published_at=published_at,
        )
