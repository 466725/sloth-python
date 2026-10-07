"""API tests for the public DSA health check endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api

HEALTH_ENDPOINTS = ("/health", "/api/health", "/api/v1/health")


class TestHealthCheck(BaseAPITest):
    """``GET /health``, ``/api/health`` and ``/api/v1/health``."""

    ENDPOINT = "/api/v1/health"
    METHOD = "get"

    @pytest.mark.parametrize("endpoint", HEALTH_ENDPOINTS)
    def test_returns_healthy_response(self, api_client: TestClient, endpoint: str) -> None:
        """Every supported health URL returns the documented payload."""
        request_started_at = datetime.now()
        response = api_client.get(endpoint)
        request_finished_at = datetime.now()

        body = self.assert_ok(response)
        assert set(body) == {"status", "timestamp"}
        assert body["status"] == "ok"

        timestamp = datetime.fromisoformat(body["timestamp"])
        assert request_started_at <= timestamp <= request_finished_at

    @pytest.mark.parametrize("endpoint", HEALTH_ENDPOINTS)
    def test_matches_published_contract(
        self, api_client: TestClient, api_spec: dict[str, Any], endpoint: str
    ) -> None:
        """The health payload validates against its api_spec.json schema."""
        response = api_client.get(endpoint)

        self.assert_matches_spec(api_spec, response, path=endpoint, method="get")

    @pytest.mark.parametrize("endpoint", HEALTH_ENDPOINTS)
    def test_remains_accessible_when_auth_enabled(
        self, auth_enabled_client: TestClient, endpoint: str
    ) -> None:
        """Health URLs stay auth-exempt so monitoring never needs a session."""
        response = auth_enabled_client.get(endpoint)

        body = self.assert_ok(response)
        assert body["status"] == "ok"

    @pytest.mark.parametrize("endpoint", HEALTH_ENDPOINTS)
    def test_rejects_unsupported_method(self, api_client: TestClient, endpoint: str) -> None:
        """Health endpoints are read-only."""
        response = api_client.post(endpoint)

        assert response.status_code == 405

    def test_is_not_shadowed_by_spa_fallback(self, api_env, api_client: TestClient) -> None:
        """``/health`` returns JSON even when a built frontend is present."""
        (api_env.static_dir / "assets").mkdir(exist_ok=True)
        (api_env.static_dir / "index.html").write_text(
            '<!doctype html><div id="root"></div>', encoding="utf-8"
        )

        from api.app import create_app

        client = TestClient(create_app(static_dir=api_env.static_dir))
        response = client.get("/health")

        body = self.assert_ok(response)
        assert body["status"] == "ok"
