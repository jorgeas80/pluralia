"""Tests for NewsGroup entity."""
import pytest
from uuid import UUID
from libs.domain.entities.news_group import NewsGroup
from libs.domain.value_objects.topic_hash import TopicHash
from libs.domain.errors.domain_error import InvalidDomainError
from tests.factories.news_group_factory import NewsGroupFactory


def test_new_creates_news_group_with_uuid(fake):
    topic_hash = TopicHash.from_title(fake.sentence())

    group = NewsGroup.new(topic_hash=topic_hash)

    assert isinstance(group.id, UUID)
    assert group.topic_hash == topic_hash
    assert group.summary is None


def test_new_generates_uuid_if_not_provided(fake):
    topic_hash = TopicHash.from_title(fake.sentence())
    group1 = NewsGroup.new(topic_hash=topic_hash)
    group2 = NewsGroup.new(topic_hash=topic_hash)

    assert group1.id != group2.id


def test_build_creates_news_group_with_existing_id(fake):
    group_id = fake.uuid4(cast_to=None)
    topic_hash = TopicHash.from_title(fake.sentence())
    summary = fake.text()

    group = NewsGroup.build(id=group_id, topic_hash=topic_hash, summary=summary, created_at=fake.date_time())

    assert group.id == group_id
    assert group.topic_hash == topic_hash
    assert group.summary == summary


@pytest.mark.parametrize("invalid_id", ["not-a-uuid", 123, None])
def test_invalid_id_raises_error(invalid_id, fake):
    topic_hash = TopicHash.from_title(fake.sentence())
    with pytest.raises(InvalidDomainError, match="NewsGroup id must be a UUID"):
        NewsGroup.build(
            id=invalid_id,
            topic_hash=topic_hash,
            summary=None,
            created_at=fake.date_time(),
        )


def test_summary_too_long_raises_error(fake):
    topic_hash = TopicHash.from_title(fake.sentence())
    long_summary = "a" * 2001

    with pytest.raises(InvalidDomainError, match="NewsGroup summary must be less than 2000 characters"):
        NewsGroup.new(topic_hash=topic_hash, summary=long_summary)


def test_news_group_is_immutable(fake):
    from dataclasses import FrozenInstanceError
    group = NewsGroupFactory.build()
    with pytest.raises(FrozenInstanceError):
        group.summary = "New Summary"

