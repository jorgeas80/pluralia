"""Factory for Article entity."""
from factory import Factory, Faker, SubFactory
from uuid import UUID, uuid4
from datetime import datetime
from libs.domain.entities.article import Article
from tests.factories.source_factory import SourceFactory


class ArticleFactory(Factory):
    """Factory for creating Article instances."""

    class Meta:
        model = Article

    id = Faker("uuid4", cast_to=None)
    title = Faker("sentence", nb_words=8)
    link = Faker("url")
    description = Faker("text", max_nb_chars=200)
    published_at = Faker("date_time")
    source_id = Faker("uuid4", cast_to=None)
    group_id = None

