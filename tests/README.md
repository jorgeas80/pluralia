# Tests

This directory contains all tests for the Pluralia project, following Domain-Driven Design principles.

## Structure

```
tests/
├── conftest.py              # Global fixtures
├── factories/               # Test data factories
│   ├── bias_factory.py
│   ├── topic_hash_factory.py
│   ├── source_factory.py
│   ├── article_factory.py
│   └── news_group_factory.py
├── unit/                    # Unit tests (fast, isolated)
│   ├── domain/
│   │   ├── entities/       # Entity tests
│   │   └── value_objects/  # Value object tests
│   └── application/         # Use case tests
└── integration/             # Integration tests
    └── api/                 # API endpoint tests
```

## Running Tests

### Option 1: Using Docker (Recommended)

```bash
# Run all tests
docker-compose --profile test run --rm pluralia-test pytest

# Run with verbose output
docker-compose --profile test run --rm pluralia-test pytest -v

# Run specific test category
docker-compose --profile test run --rm pluralia-test pytest tests/unit
docker-compose --profile test run --rm pluralia-test pytest tests/integration

# Run specific test file
docker-compose --profile test run --rm pluralia-test pytest tests/unit/domain/entities/test_source.py

# Run with coverage
docker-compose --profile test run --rm pluralia-test pytest --cov=libs --cov=services --cov-report=html
```

### Option 2: Local Development

#### Install Dependencies

```bash
pip install -r tests/requirements.txt
```

#### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit

# Integration tests only
pytest tests/integration

# Specific test file
pytest tests/unit/domain/entities/test_source.py

# Specific test
pytest tests/unit/domain/entities/test_source.py::test_new_creates_source_with_uuid
```

### Run with Coverage

```bash
pytest --cov=libs --cov=services --cov-report=html
```

### Run with Verbose Output

```bash
pytest -v
```

## Test Categories

### Unit Tests

- **Domain Entities**: Test business logic, validation, and immutability
- **Value Objects**: Test validation and behavior
- **Use Cases**: Test application logic with mocked dependencies

### Integration Tests

- **API Endpoints**: Test HTTP endpoints end-to-end
- **Database**: Test repository implementations with real database

## Test Data

Tests use **Factory Boy** and **Faker** for generating test data:

```python
from tests.factories.source_factory import SourceFactory

source = SourceFactory.build()
source_with_overrides = SourceFactory.build(name="Custom Name", bias=Bias.right())
```

## Fixtures

Global fixtures are defined in `conftest.py`:
- `fake`: Faker instance for generating random data

Application-level fixtures in `tests/unit/application/conftest.py`:
- `mock_article_repository`: Mock ArticleRepository
- `mock_source_repository`: Mock SourceRepository

## Writing Tests

Follow the AAA pattern (Arrange-Act-Assert) and use descriptive test names:

```python
def test_new_creates_source_with_uuid(fake):
    # Arrange
    name = fake.company()
    bias = Bias.left()
    
    # Act
    source = Source.new(name=name, url=None, bias=bias)
    
    # Assert
    assert isinstance(source.id, UUID)
    assert source.name == name
```

## Test Database

Integration tests require a test database. Set the `TEST_DATABASE_URL` environment variable:

```bash
export TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/pluralia_test"
```

The test database is automatically created and cleaned between tests.

