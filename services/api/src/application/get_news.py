from libs.domain.repositories.article_repository import ArticleRepository
from libs.domain.repositories.source_repository import SourceRepository


class GetNews:
    """Use case for getting news articles."""

    def __init__(
        self,
        article_repository: ArticleRepository,
        source_repository: SourceRepository,
    ):
        self._article_repository = article_repository
        self._source_repository = source_repository

    async def execute(self, limit: int = 20) -> list[dict]:
        """Gets recent news from all sources."""
        sources = await self._source_repository.find_all()
        all_articles = []

        for source in sources:
            articles = await self._article_repository.find_by_source_id(source.id, limit=limit)
            for article in articles:
                all_articles.append({
                    "id": str(article.id),
                    "title": article.title,
                    "link": article.link,
                    "description": article.description,
                    "published": article.published_at.isoformat() if article.published_at else None,
                    "source": source.name,
                    "bias": source.bias.value,
                })

        return all_articles

