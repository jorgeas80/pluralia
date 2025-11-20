from typing import Optional
from uuid import UUID, uuid5, NAMESPACE_DNS
from sqlmodel import Session, select

from libs.domain.entities.news_group import NewsGroup
from libs.domain.repositories.news_group_repository import NewsGroupRepository
from libs.domain.value_objects.topic_hash import TopicHash
from services.ingest.src.infrastructure.database.models import NewsGroupModel


class SqlModelNewsGroupRepository(NewsGroupRepository):
    def __init__(self, session: Session):
        self._session = session

    async def save(self, group: NewsGroup) -> None:
        # Check if exists first by topic_hash (unique field)
        existing = await self.find_by_topic_hash(group.topic_hash)
        if existing:
            # Group already exists, no need to save again
            return
        
        # Add new group
        group_model = self._to_model(group)
        self._session.add(group_model)
        self._session.commit()
        self._session.refresh(group_model)

    async def find_by_id(self, group_id: UUID) -> Optional[NewsGroup]:
        result = self._session.exec(select(NewsGroupModel).where(NewsGroupModel.id == str(group_id))).first()
        return self._to_entity(result) if result else None

    async def find_by_topic_hash(self, topic_hash: TopicHash) -> Optional[NewsGroup]:
        result = self._session.exec(
            select(NewsGroupModel).where(NewsGroupModel.topic_hash == topic_hash.value)
        ).first()
        return self._to_entity(result) if result else None

    def _to_model(self, group: NewsGroup) -> NewsGroupModel:
        return NewsGroupModel(
            id=str(group.id),
            topic_hash=group.topic_hash.value,
            summary=group.summary,
            created_at=group.created_at,
        )

    def _to_entity(self, model: NewsGroupModel) -> NewsGroup:
        # Handle both int (from existing DB stored as string) and str (UUID) IDs
        try:
            # Try to parse as int first (for existing data)
            int_id = int(model.id)
            model_id = uuid5(NAMESPACE_DNS, f"newsgroup-{int_id}")
        except (ValueError, TypeError):
            # Not an int, try to parse as UUID
            try:
                model_id = UUID(model.id)
            except (ValueError, AttributeError):
                model_id = uuid5(NAMESPACE_DNS, f"newsgroup-{model.id}")
        
        return NewsGroup.build(
            id=model_id,
            topic_hash=TopicHash(value=model.topic_hash),
            summary=model.summary,
            created_at=model.created_at,
        )

