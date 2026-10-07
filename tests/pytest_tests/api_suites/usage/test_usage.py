"""API tests for the LLM usage reporting endpoints."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from ai_stock.storage import DatabaseManager
from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api

VALID_PERIODS = ("today", "month", "all")


@pytest.fixture
def seeded_usage(db_manager: DatabaseManager) -> DatabaseManager:
    """Record two LLM calls so aggregation has deterministic input."""
    db_manager.record_llm_usage(
        call_type="analysis",
        model="gemini-2.0-flash",
        prompt_tokens=100,
        completion_tokens=50,
        total_tokens=150,
        stock_code="600519",
    )
    db_manager.record_llm_usage(
        call_type="news",
        model="gpt-4o-mini",
        prompt_tokens=20,
        completion_tokens=10,
        total_tokens=30,
        stock_code="000858",
    )
    return db_manager


class TestUsageSummary(BaseAPITest):
    """``GET /api/v1/usage/summary``."""

    ENDPOINT = "/api/v1/usage/summary"
    METHOD = "get"

    def test_returns_empty_summary_without_usage(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A fresh database reports zeroed totals rather than failing."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["period"] == "month"
        assert body["total_calls"] == 0
        assert body["total_tokens"] == 0
        assert body["by_call_type"] == []
        assert body["by_model"] == []

    def test_aggregates_recorded_calls(
        self, api_client: TestClient, seeded_usage: DatabaseManager
    ) -> None:
        """Totals and breakdowns reflect every call inside the period."""
        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"period": "all"}))

        assert body["total_calls"] == 2
        assert body["total_prompt_tokens"] == 120
        assert body["total_completion_tokens"] == 60
        assert body["total_tokens"] == 180
        assert {entry["call_type"] for entry in body["by_call_type"]} == {"analysis", "news"}
        assert {entry["model"] for entry in body["by_model"]} == {
            "gemini-2.0-flash",
            "gpt-4o-mini",
        }

    @pytest.mark.parametrize("period", VALID_PERIODS)
    def test_accepts_every_supported_period(
        self, api_client: TestClient, api_spec: dict[str, Any], period: str
    ) -> None:
        """Each documented period returns a well-formed window."""
        response = api_client.get(self.ENDPOINT, params={"period": period})

        body = self.assert_matches_spec(api_spec, response)
        assert body["period"] == period
        assert body["from_date"] <= body["to_date"]

    def test_unknown_period_falls_back_to_month(self, api_client: TestClient) -> None:
        """Unsupported period values degrade to the default month window."""
        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"period": "decade"}))

        assert body["period"] == "month"


class TestUsageDashboard(BaseAPITest):
    """``GET /api/v1/usage/dashboard``."""

    ENDPOINT = "/api/v1/usage/dashboard"
    METHOD = "get"

    def test_returns_summary_with_recent_calls(
        self, api_client: TestClient, api_spec: dict[str, Any], seeded_usage: DatabaseManager
    ) -> None:
        """The dashboard extends the summary payload with call records."""
        response = api_client.get(self.ENDPOINT, params={"period": "all"})

        body = self.assert_matches_spec(api_spec, response)
        assert body["total_calls"] == 2
        assert len(body["recent_calls"]) == 2
        for record in body["recent_calls"]:
            assert isinstance(record["called_at"], str) and record["called_at"]
            assert record["model"]

    def test_limit_caps_returned_records(
        self, api_client: TestClient, seeded_usage: DatabaseManager
    ) -> None:
        """``limit`` restricts only the record list, not the aggregates."""
        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"period": "all", "limit": 1}))

        assert body["total_calls"] == 2
        assert len(body["recent_calls"]) == 1

    @pytest.mark.parametrize("limit", [0, -1, 201])
    def test_rejects_out_of_range_limit(self, api_client: TestClient, limit: int) -> None:
        """``limit`` is constrained to the documented 1..200 range."""
        response = api_client.get(self.ENDPOINT, params={"limit": limit})

        self.assert_validation_error(response, field="limit")
