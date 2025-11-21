"""Factory for NewsGroup entity."""
from factory import Factory, Faker, SubFactory
from uuid import UUID, uuid4
from datetime import datetime
from libs.domain.entities.news_group import NewsGroup
from tests.factories.topic_hash_factory import TopicHashFactory


class NewsGroupFactory(Factory):
    """Factory for creating NewsGroup instances."""

    class Meta:
        model = NewsGroup

    id = Faker("uuid4", cast_to=None)
    topic_hash = SubFactory(TopicHashFactory)
    summary = Faker("text", max_nb_chars=500)
    created_at = Faker("date_time")

