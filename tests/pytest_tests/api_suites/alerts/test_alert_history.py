"""API tests for the alert trigger and notification history endpoints."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api


class TestListAlertTriggers(BaseAPITest):
    """``GET /api/v1/alerts/triggers``."""

    ENDPOINT = "/api/v1/alerts/triggers"
    METHOD = "get"

    def test_returns_empty_page(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """Without any fired alerts the history is an empty page."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert self.assert_paginated(body, page=1) == []
        assert body["page_size"] == 20

    @pytest.mark.parametrize(
        "params",
        [
            {"rule_id": 1},
            {"target": "600519"},
            {"status": "triggered"},
            {"rule_id": 1, "target": "600519", "status": "notified"},
        ],
    )
    def test_accepts_documented_filters(
        self, api_client: TestClient, api_spec: dict[str, Any], params: dict[str, Any]
    ) -> None:
        """Every documented filter combination is accepted."""
        response = api_client.get(self.ENDPOINT, params=params)

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == 0

    @pytest.mark.parametrize(
        ("field", "value"),
        [("page", 0), ("page_size", 0), ("page_size", 101), ("rule_id", "abc")],
    )
    def test_rejects_invalid_query_parameters(
        self, api_client: TestClient, field: str, value: Any
    ) -> None:
        """Documented query bounds and types are enforced."""
        response = api_client.get(self.ENDPOINT, params={field: value})

        self.assert_validation_error(response, field=field)


class TestListAlertNotifications(BaseAPITest):
    """``GET /api/v1/alerts/notifications``."""

    ENDPOINT = "/api/v1/alerts/notifications"
    METHOD = "get"

    def test_returns_empty_page(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """Without delivery attempts the history is an empty page."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert self.assert_paginated(body, page=1) == []
        assert body["page_size"] == 20

    @pytest.mark.parametrize(
        "params",
        [
            {"trigger_id": 1},
            {"channel": "wechat"},
            {"success": "true"},
            {"success": "false"},
        ],
    )
    def test_accepts_documented_filters(
        self, api_client: TestClient, api_spec: dict[str, Any], params: dict[str, Any]
    ) -> None:
        """Every documented filter combination is accepted."""
        response = api_client.get(self.ENDPOINT, params=params)

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == 0

    @pytest.mark.parametrize(
        ("field", "value"),
        [("page", 0), ("page_size", 0), ("page_size", 101), ("trigger_id", "abc")],
    )
    def test_rejects_invalid_query_parameters(
        self, api_client: TestClient, field: str, value: Any
    ) -> None:
        """Documented query bounds and types are enforced."""
        response = api_client.get(self.ENDPOINT, params={field: value})

        self.assert_validation_error(response, field=field)
