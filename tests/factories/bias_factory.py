"""Factory for Bias value object."""
from factory import Factory
from libs.domain.value_objects.bias import Bias


class BiasFactory(Factory):
    """Factory for creating Bias instances."""

    class Meta:
        model = Bias

    value = "left"

