from datetime import datetime, timedelta, timezone


NEWS_RETENTION_DAYS = 7


def news_retention_cutoff(now: datetime | None = None) -> datetime:
    """Return the UTC cutoff for data considered current news."""
    current_time = now or datetime.now(timezone.utc)
    if current_time.utcoffset() is None:
        raise ValueError("now must include timezone information")
    return current_time.astimezone(timezone.utc) - timedelta(days=NEWS_RETENTION_DAYS)
