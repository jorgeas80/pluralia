from typing import Optional
from uuid import UUID, uuid5, NAMESPACE_DNS
from sqlmodel import Session, select

from libs.domain.entities.source import Source
from libs.domain.repositories.source_repository import SourceRepository
from libs.domain.value_objects.bias import Bias
from services.api.src.infrastructure.database.models import SourceModel


class SqlModelSourceRepository(SourceRepository):
    def __init__(self, session: Session):
        self._session = session

    async def save(self, source: Source) -> None:
        source_model = self._to_model(source)
        self._session.merge(source_model)
        self._session.commit()
        self._session.refresh(source_model)

    async def find_by_id(self, source_id: UUID) -> Optional[Source]:
        result = self._session.exec(select(SourceModel).where(SourceModel.id == str(source_id))).first()
        return self._to_entity(result) if result else None

    async def find_by_name(self, name: str) -> Optional[Source]:
        result = self._session.exec(select(SourceModel).where(SourceModel.name == name)).first()
        return self._to_entity(result) if result else None

    async def find_all(self) -> list[Source]:
        results = self._session.exec(select(SourceModel)).all()
        return [self._to_entity(model) for model in results]

    def _to_model(self, source: Source) -> SourceModel:
        return SourceModel(
            id=str(source.id),
            name=source.name,
            url=source.url,
            bias=source.bias.value,
        )

    def _to_entity(self, model: SourceModel) -> Source:
        bias = Bias.left() if model.bias == "left" else (Bias.center() if model.bias == "center" else Bias.right())
        # Handle both int (from existing DB stored as string) and str (UUID) IDs
        try:
            # Try to parse as int first (for existing data)
            int_id = int(model.id)
            # Generate deterministic UUID from int
            model_id = uuid5(NAMESPACE_DNS, f"source-{int_id}")
        except (ValueError, TypeError):
            # Not an int, try to parse as UUID
            try:
                model_id = UUID(model.id)
            except (ValueError, AttributeError):
                # Fallback: generate UUID from string
                model_id = uuid5(NAMESPACE_DNS, f"source-{model.id}")
        
        return Source.build(
            id=model_id,
            name=model.name,
            url=model.url,
            bias=bias,
        )

