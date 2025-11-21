"""Global test fixtures."""
import pytest
from faker import Faker

faker = Faker()


@pytest.fixture
def fake():
    """Faker instance for generating test data."""
    return faker

