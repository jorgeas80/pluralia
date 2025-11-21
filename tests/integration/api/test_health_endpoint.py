"""Integration tests for health endpoint."""
import pytest
from fastapi.testclient import TestClient
from services.api.src.main import app


@pytest.fixture
def client():
    """Test client for API."""
    return TestClient(app)


def test_health_endpoint_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

