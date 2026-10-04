"""API tests for the public DSA health check endpoints."""

from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.app import create_app

HEALTH_ENDPOINTS = ("/health", "/api/health", "/api/v1/health")

pytestmark = pytest.mark.api


@pytest.fixture
def api_client(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> TestClient:
    """Create an isolated API client with admin authentication enabled."""
    monkeypatch.setattr("api.middlewares.auth.is_auth_enabled", lambda: True)
    return TestClient(create_app(static_dir=tmp_path))


@pytest.mark.parametrize("endpoint", HEALTH_ENDPOINTS)
def test_health_endpoint_returns_healthy_response(
    api_client: TestClient, endpoint: str
) -> None:
    """Every supported health URL returns the documented, auth-exempt response."""
    request_started_at = datetime.now()
    response = api_client.get(endpoint)
    request_finished_at = datetime.now()

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    body = response.json()
    assert set(body) == {"status", "timestamp"}
    assert body["status"] == "ok"

    timestamp = datetime.fromisoformat(body["timestamp"])
    assert request_started_at <= timestamp <= request_finished_at
