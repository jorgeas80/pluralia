from uuid import uuid4

import feedparser
import pytest

from services.ingest.src.infrastructure.services.rss_parser import RSSParser
from services.ingest.src.infrastructure.services.rss_parser import UndatedArticleError


@pytest.mark.parametrize("date, expected", [
    ("Sun, 27 Sep 2026 10:00:00 +0200", "2026-09-27T08:00:00+00:00"),
    ("Sun, 25 Oct 2026 02:30:00 +0200", "2026-10-25T00:30:00+00:00"),
    ("Sun, 25 Oct 2026 02:30:00 +0100", "2026-10-25T01:30:00+00:00"),
    ("Sun, 27 Sep 2026 23:30:00 -0500", "2026-09-28T04:30:00+00:00"),
    ("Sun, 27 Sep 2026 08:00:00 GMT", "2026-09-27T08:00:00+00:00"),
])
def test_rss_dates_preserve_instant_in_utc(date, expected):
    date_element = f"<pubDate>{date}</pubDate>" if date else ""
    feed = feedparser.parse(f"""<rss version="2.0"><channel><title>Example</title>
        <item><title>Story</title><link>https://example.com/story</link>
        {date_element}</item></channel></rss>""")
    article = RSSParser.entry_to_article(feed.entries[0], uuid4())
    actual = article.published_at.isoformat() if article.published_at else None
    assert actual == expected


@pytest.mark.parametrize("date", ["invalid", None])
def test_rss_entries_without_a_valid_publication_date_are_rejected(date):
    entry = feedparser.FeedParserDict({
        "title": "Story",
        "link": "https://example.com/story",
        "published": date,
        "published_parsed": None,
    })

    with pytest.raises(UndatedArticleError):
        RSSParser.entry_to_article(entry, uuid4())
