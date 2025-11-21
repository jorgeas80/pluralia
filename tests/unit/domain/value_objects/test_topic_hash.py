"""Tests for TopicHash value object."""
import pytest
from libs.domain.value_objects.topic_hash import TopicHash
from libs.domain.errors.domain_error import InvalidDomainError


def test_from_title_creates_hash_from_title():
    title = "Test News Title"
    topic_hash = TopicHash.from_title(title)
    assert isinstance(topic_hash.value, str)
    assert len(topic_hash.value) == 16


def test_from_title_normalizes_to_lowercase():
    title1 = "Test News Title"
    title2 = "TEST NEWS TITLE"
    hash1 = TopicHash.from_title(title1)
    hash2 = TopicHash.from_title(title2)
    assert hash1.value == hash2.value


def test_from_title_strips_whitespace():
    title1 = "  Test News Title  "
    title2 = "Test News Title"
    hash1 = TopicHash.from_title(title1)
    hash2 = TopicHash.from_title(title2)
    assert hash1.value == hash2.value


def test_same_title_produces_same_hash():
    title = "Test News Title"
    hash1 = TopicHash.from_title(title)
    hash2 = TopicHash.from_title(title)
    assert hash1.value == hash2.value


def test_different_titles_produce_different_hashes():
    title1 = "Test News Title One"
    title2 = "Test News Title Two"
    hash1 = TopicHash.from_title(title1)
    hash2 = TopicHash.from_title(title2)
    assert hash1.value != hash2.value


@pytest.mark.parametrize("invalid_value", ["", "short", "a" * 15, "a" * 17])
def test_invalid_hash_length_raises_error(invalid_value):
    with pytest.raises(InvalidDomainError, match="TopicHash must be exactly 16 characters"):
        TopicHash(value=invalid_value)


def test_topic_hash_is_immutable():
    from dataclasses import FrozenInstanceError
    topic_hash = TopicHash.from_title("Test Title")
    with pytest.raises(FrozenInstanceError):
        topic_hash.value = "newvalue123456"

