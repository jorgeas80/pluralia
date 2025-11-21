"""Tests for Bias value object."""
import pytest
from libs.domain.value_objects.bias import Bias
from libs.domain.errors.domain_error import InvalidDomainError


def test_left_creates_bias_with_left_value():
    bias = Bias.left()
    assert bias.value == "left"


def test_center_creates_bias_with_center_value():
    bias = Bias.center()
    assert bias.value == "center"


def test_right_creates_bias_with_right_value():
    bias = Bias.right()
    assert bias.value == "right"


@pytest.mark.parametrize("invalid_value", ["invalid", "left-center", "", "LEFT"])
def test_invalid_bias_value_raises_error(invalid_value):
    with pytest.raises(InvalidDomainError, match="Bias must be one of"):
        Bias(value=invalid_value)


def test_bias_is_immutable():
    from dataclasses import FrozenInstanceError
    bias = Bias.left()
    with pytest.raises(FrozenInstanceError):
        bias.value = "right"

