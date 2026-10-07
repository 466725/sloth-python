"""API tests for the decision-signal outcome evaluation endpoints."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api


class TestRunOutcomes(BaseAPITest):
    """``POST /api/v1/decision-signals/outcomes/run``."""

    ENDPOINT = "/api/v1/decision-signals/outcomes/run"
    METHOD = "post"

    def test_no_signals_evaluates_nothing(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """An empty signal store short-circuits without fetching market data."""
        response = api_client.post(self.ENDPOINT, json={})

        body = self.assert_matches_spec(api_spec, response)
        assert body["evaluated"] == 0
        assert body["created"] == 0
        assert body["updated"] == 0
        assert body["items"] == []
        assert body["engine_version"]

    def test_unmatched_filters_evaluate_nothing(self, api_client: TestClient) -> None:
        """Filters that match no signal are a safe no-op."""
        payload = {"market": "cn", "stock_code": "999999", "action": "buy", "limit": 10}

        body = self.assert_ok(api_client.post(self.ENDPOINT, json=payload))

        assert body["evaluated"] == 0

    @pytest.mark.parametrize(
        ("payload", "field"),
        [
            ({"signal_id": 0}, "signal_id"),
            ({"limit": 0}, "limit"),
            ({"limit": 501}, "limit"),
            ({"horizons": ["2y"]}, "horizons"),
            ({"market": "eu"}, "market"),
            ({"action": "hodl"}, "action"),
            ({"source_type": "rumor"}, "source_type"),
            ({"status": "paused"}, "status"),
        ],
    )
    def test_rejects_values_outside_the_schema(
        self, api_client: TestClient, payload: dict[str, Any], field: str
    ) -> None:
        """Enumerations and numeric bounds are validated before evaluation."""
        response = api_client.post(self.ENDPOINT, json=payload)

        self.assert_validation_error(response, field=field)

    def test_requires_authentication_when_enabled(
        self, auth_enabled_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Without a session cookie the endpoint reports ``401``."""
        response = auth_enabled_client.post(self.ENDPOINT, json={})

        self.assert_unauthorized(response)
        self.assert_documented_status(api_spec, response)


class TestListOutcomes(BaseAPITest):
    """``GET /api/v1/decision-signals/outcomes``."""

    ENDPOINT = "/api/v1/decision-signals/outcomes"
    METHOD = "get"

    def test_returns_empty_page(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """Without evaluations the outcome history is an empty page."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert self.assert_paginated(body, page=1) == []

    @pytest.mark.parametrize(
        "params",
        [
            {"signal_id": 1},
            {"horizon": "5d"},
            {"engine_version": "v1"},
            {"eval_status": "completed"},
            {"outcome": "hit"},
        ],
    )
    def test_accepts_documented_filters(
        self, api_client: TestClient, api_spec: dict[str, Any], params: dict[str, Any]
    ) -> None:
        """Every documented filter is accepted."""
        response = api_client.get(self.ENDPOINT, params=params)

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == 0

    @pytest.mark.parametrize(
        ("field", "value"),
        [("page", 0), ("page_size", 0), ("page_size", 101), ("signal_id", 0)],
    )
    def test_rejects_invalid_query_parameters(
        self, api_client: TestClient, field: str, value: int
    ) -> None:
        """Documented query bounds are enforced."""
        response = api_client.get(self.ENDPOINT, params={field: value})

        self.assert_validation_error(response, field=field)


class TestOutcomeStats(BaseAPITest):
    """``GET /api/v1/decision-signals/outcomes/stats``."""

    ENDPOINT = "/api/v1/decision-signals/outcomes/stats"
    METHOD = "get"

    def test_returns_zeroed_statistics(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Without evaluations every counter is zero."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == 0
        assert body["completed"] == 0
        assert body["hit"] == 0
        assert body["miss"] == 0
        assert body["engine_version"]

    def test_accepts_repeated_list_parameters(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """``horizons`` and ``statuses`` accept repeated query values."""
        response = api_client.get(
            self.ENDPOINT,
            params=[("horizons", "1d"), ("horizons", "5d"), ("statuses", "active")],
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["horizons"] == ["1d", "5d"]

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Without a session cookie the endpoint reports ``401``."""
        self.assert_unauthorized(auth_enabled_client.get(self.ENDPOINT))


class TestSignalOutcomes(BaseAPITest):
    """``GET /api/v1/decision-signals/{signal_id}/outcomes``."""

    ENDPOINT = "/api/v1/decision-signals/{signal_id}/outcomes"
    METHOD = "get"

    def test_returns_empty_list_for_unevaluated_signal(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_signal: Callable[..., dict[str, Any]],
    ) -> None:
        """A signal without evaluations returns an empty list."""
        signal = create_signal()

        response = api_client.get(f"/api/v1/decision-signals/{signal['id']}/outcomes")

        body = self.assert_matches_spec(api_spec, response)
        assert body["items"] == []
        assert body["total"] == 0

    def test_returns_404_for_unknown_signal(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Unknown ids report a documented ``404``."""
        response = api_client.get("/api/v1/decision-signals/999999/outcomes")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)

    def test_rejects_non_integer_signal_id(self, api_client: TestClient) -> None:
        """``signal_id`` must be an integer path parameter."""
        response = api_client.get("/api/v1/decision-signals/not-a-number/outcomes")

        self.assert_validation_error(response, field="signal_id")
