"""API tests for the backtest endpoints."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api


class TestRunBacktest(BaseAPITest):
    """``POST /api/v1/backtest/run``."""

    ENDPOINT = "/api/v1/backtest/run"
    METHOD = "post"

    def test_returns_zeroed_stats_without_history(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Running against an empty history reports no processed records."""
        response = api_client.post(self.ENDPOINT, json={})

        body = self.assert_matches_spec(api_spec, response)
        assert body == {
            "processed": 0,
            "saved": 0,
            "completed": 0,
            "insufficient": 0,
            "errors": 0,
        }

    def test_accepts_documented_filters(self, api_client: TestClient) -> None:
        """Optional filters are honored without changing the response shape."""
        payload = {"code": "600519", "force": True, "eval_window_days": 5, "limit": 10}

        body = self.assert_ok(api_client.post(self.ENDPOINT, json=payload))

        assert body["processed"] == 0

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("eval_window_days", 0),
            ("eval_window_days", 121),
            ("min_age_days", -1),
            ("min_age_days", 366),
            ("limit", 0),
            ("limit", 2001),
        ],
    )
    def test_rejects_out_of_range_values(
        self, api_client: TestClient, field: str, value: int
    ) -> None:
        """Documented numeric bounds are enforced before any work starts."""
        response = api_client.post(self.ENDPOINT, json={field: value})

        self.assert_validation_error(response, field=field)


class TestBacktestResults(BaseAPITest):
    """``GET /api/v1/backtest/results``."""

    ENDPOINT = "/api/v1/backtest/results"
    METHOD = "get"

    def test_returns_empty_page(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """An empty result set still returns a valid pagination envelope."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert self.assert_paginated(body, page=1) == []
        assert body["limit"] == 20

    def test_rejects_inverted_analysis_date_range(self, api_client: TestClient) -> None:
        """``analysis_date_from`` may not be later than ``analysis_date_to``."""
        response = api_client.get(
            self.ENDPOINT,
            params={"analysis_date_from": "2026-02-01", "analysis_date_to": "2026-01-01"},
        )

        self.assert_error(response, 400, "invalid_params")

    def test_rejects_unknown_analysis_phase(self, api_client: TestClient) -> None:
        """``analysis_phase`` is restricted to the documented enumeration."""
        response = api_client.get(self.ENDPOINT, params={"analysis_phase": "lunch_break"})

        self.assert_validation_error(response, field="analysis_phase")

    @pytest.mark.parametrize(("field", "value"), [("page", 0), ("limit", 0), ("limit", 201)])
    def test_rejects_invalid_pagination(
        self, api_client: TestClient, field: str, value: int
    ) -> None:
        """Pagination bounds documented in api_spec.json are enforced."""
        response = api_client.get(self.ENDPOINT, params={field: value})

        self.assert_validation_error(response, field=field)


class TestOverallPerformance(BaseAPITest):
    """``GET /api/v1/backtest/performance``."""

    ENDPOINT = "/api/v1/backtest/performance"
    METHOD = "get"

    def test_returns_404_without_summary(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """No computed summary yields a documented ``404``."""
        response = api_client.get(self.ENDPOINT)

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)

    def test_rejects_inverted_analysis_date_range(self, api_client: TestClient) -> None:
        """Date-range validation happens before summary lookup."""
        response = api_client.get(
            self.ENDPOINT,
            params={"analysis_date_from": "2026-05-05", "analysis_date_to": "2026-05-01"},
        )

        self.assert_error(response, 400, "invalid_params")

    @pytest.mark.parametrize("eval_window_days", [0, 121])
    def test_rejects_out_of_range_window(
        self, api_client: TestClient, eval_window_days: int
    ) -> None:
        """``eval_window_days`` honors the documented 1..120 range."""
        response = api_client.get(self.ENDPOINT, params={"eval_window_days": eval_window_days})

        self.assert_validation_error(response, field="eval_window_days")


class TestStockPerformance(BaseAPITest):
    """``GET /api/v1/backtest/performance/{code}``."""

    ENDPOINT = "/api/v1/backtest/performance/{code}"
    METHOD = "get"

    def test_returns_404_for_stock_without_summary(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """An unevaluated stock reports ``404`` instead of empty metrics."""
        response = api_client.get("/api/v1/backtest/performance/600519")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)

    def test_rejects_inverted_analysis_date_range(self, api_client: TestClient) -> None:
        """Per-stock queries share the overall date-range validation."""
        response = api_client.get(
            "/api/v1/backtest/performance/600519",
            params={"analysis_date_from": "2026-05-05", "analysis_date_to": "2026-05-01"},
        )

        self.assert_error(response, 400, "invalid_params")
