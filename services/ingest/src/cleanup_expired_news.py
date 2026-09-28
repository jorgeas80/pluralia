from services.ingest.src.application.cleanup_old_news import cleanup_old_news
from services.ingest.src.infrastructure.database.db import get_session


def main() -> None:
    with get_session() as session:
        deleted_articles, deleted_groups = cleanup_old_news(session)
    print(
        "Live-news cleanup complete: "
        f"deleted {deleted_articles} expired articles and {deleted_groups} empty groups"
    )


if __name__ == "__main__":
    main()
