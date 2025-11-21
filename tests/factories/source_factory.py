"""Factory for Source entity."""
from factory import Factory, Faker, SubFactory
from uuid import UUID, uuid4
from libs.domain.entities.source import Source
from tests.factories.bias_factory import BiasFactory


class SourceFactory(Factory):
    """Factory for creating Source instances."""

    class Meta:
        model = Source

    id = Faker("uuid4", cast_to=None)
    name = Faker("company")
    url = Faker("url")
    bias = SubFactory(BiasFactory)

