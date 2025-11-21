"""Tests for Source entity."""
import pytest
from uuid import UUID
from libs.domain.entities.source import Source
from libs.domain.value_objects.bias import Bias
from libs.domain.errors.domain_error import InvalidDomainError
from tests.factories.source_factory import SourceFactory


def test_new_creates_source_with_uuid(fake):
    name = fake.company()
    url = fake.url()
    bias = Bias.left()

    source = Source.new(name=name, url=url, bias=bias)

    assert isinstance(source.id, UUID)
    assert source.name == name
    assert source.url == url
    assert source.bias == bias


def test_new_generates_uuid_if_not_provided(fake):
    source1 = Source.new(name=fake.company(), url=fake.url(), bias=Bias.left())
    source2 = Source.new(name=fake.company(), url=fake.url(), bias=Bias.left())

    assert source1.id != source2.id


def test_build_creates_source_with_existing_id(fake):
    source_id = fake.uuid4(cast_to=None)
    name = fake.company()
    url = fake.url()
    bias = Bias.center()

    source = Source.build(id=source_id, name=name, url=url, bias=bias)

    assert source.id == source_id
    assert source.name == name
    assert source.url == url
    assert source.bias == bias


@pytest.mark.parametrize("invalid_id", ["not-a-uuid", 123, None])
def test_invalid_id_raises_error(invalid_id, fake):
    with pytest.raises(InvalidDomainError, match="Source id must be a UUID"):
        Source.build(id=invalid_id, name=fake.company(), url=fake.url(), bias=Bias.left())


@pytest.mark.parametrize("invalid_name", ["", " " * 201, None])
def test_invalid_name_raises_error(invalid_name, fake):
    with pytest.raises(InvalidDomainError, match="Source name must be between 1 and 200 characters"):
        Source.new(name=invalid_name, url=fake.url(), bias=Bias.left())


def test_source_is_immutable(fake):
    from dataclasses import FrozenInstanceError
    source = SourceFactory.build()
    with pytest.raises(FrozenInstanceError):
        source.name = "New Name"

