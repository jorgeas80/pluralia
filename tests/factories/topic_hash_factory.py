"""Factory for TopicHash value object."""
from factory import Factory
from libs.domain.value_objects.topic_hash import TopicHash


class TopicHashFactory(Factory):
    """Factory for creating TopicHash instances."""

    class Meta:
        model = TopicHash

    value = "a1b2c3d4e5f6g7h8"

