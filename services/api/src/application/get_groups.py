from sqlmodel import Session, select

from services.api.src.infrastructure.database.models import ArticleModel, NewsGroupModel, SourceModel


class GetGroups:
    """Use case for getting news groups with their articles."""

    def __init__(self, session: Session):
        self._session = session

    async def execute(self, limit: int = 50, min_articles: int = 2) -> list[dict]:
        """Returns news groups sorted by number of articles, most covered first."""
        rows = self._session.exec(
            select(ArticleModel, SourceModel)
            .join(SourceModel, ArticleModel.source_id == SourceModel.id, isouter=True)
            .where(ArticleModel.group_id.is_not(None))
        ).all()

        # Group articles by group_id
        groups_dict: dict[str, list[dict]] = {}
        for article, source in rows:
            gid = article.group_id
            if gid not in groups_dict:
                groups_dict[gid] = []
            groups_dict[gid].append({
                "id": article.id,
                "title": article.title,
                "link": article.link,
                "description": article.description,
                "published": article.published_at.isoformat() if article.published_at else None,
                "source": source.name if source else "Desconocido",
                "bias": source.bias if source else "center",
                "sensationalism_score": article.sensationalism_score,
                "sensationalism_explanation": article.sensationalism_explanation,
            })

        # Fetch group metadata for the groups that pass the filter
        qualifying_ids = [gid for gid, arts in groups_dict.items() if len(arts) >= min_articles]
        newsgroups = self._session.exec(
            select(NewsGroupModel).where(NewsGroupModel.id.in_(qualifying_ids))
        ).all()
        newsgroup_map = {ng.id: ng for ng in newsgroups}

        output = [
            {
                "id": gid,
                "created_at": newsgroup_map[gid].created_at.isoformat() if gid in newsgroup_map else None,
                "articles": groups_dict[gid],
            }
            for gid in qualifying_ids
        ]
        output.sort(key=lambda g: len(g["articles"]), reverse=True)
        return output[:limit]
