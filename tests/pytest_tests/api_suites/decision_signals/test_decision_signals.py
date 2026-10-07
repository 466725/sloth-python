"""API tests for the decision-signal CRUD and feedback endpoints."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest
from tests.pytest_tests.api_suites.decision_signals.conftest import valid_signal_payload

pytestmark = pytest.mark.api


class TestCreateDecisionSignal(BaseAPITest):
    """``POST /api/v1/decision-signals``."""

    ENDPOINT = "/api/v1/decision-signals"
    METHOD = "post"

    def test_creates_signal(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """A valid payload is stored and reported as newly created."""
        response = api_client.post(self.ENDPOINT, json=valid_signal_payload())

        body = self.assert_matches_spec(api_spec, response)
        assert body["created"] is True
        item = body["item"]
        assert item["id"] > 0
        assert item["stock_code"] == "600519"
        assert item["action"] == "buy"
        assert item["status"] == "active"

    def test_rejects_missing_required_fields(self, api_client: TestClient) -> None:
        """``stock_code``, ``market``, ``source_type``, ``trigger_source`` and ``action`` are required."""
        response = api_client.post(self.ENDPOINT, json={})

        body = self.assert_validation_error(response)
        missing = {entry["loc"][-1] for entry in body["detail"]}
        assert {"stock_code", "market", "source_type", "trigger_source", "action"} <= missing

    @pytest.mark.parametrize(
        ("overrides", "field"),
        [
            ({"market": "eu"}, "market"),
            ({"source_type": "rumor"}, "source_type"),
            ({"horizon": "2y"}, "horizon"),
            ({"status": "paused"}, "status"),
            ({"plan_quality": "perfect"}, "plan_quality"),
            ({"confidence": 1.5}, "confidence"),
            ({"confidence": -0.1}, "confidence"),
            ({"score": 101}, "score"),
            ({"entry_low": 0}, "entry_low"),
            ({"stop_loss": -1}, "stop_loss"),
            ({"stock_code": ""}, "stock_code"),
            ({"trigger_source": ""}, "trigger_source"),
        ],
    )
    def test_rejects_values_outside_the_schema(
        self, api_client: TestClient, overrides: dict[str, Any], field: str
    ) -> None:
        """Enumerations and numeric bounds documented in api_spec.json are enforced."""
        response = api_client.post(self.ENDPOINT, json=valid_signal_payload(**overrides))

        self.assert_validation_error(response, field=field)

    def test_requires_authentication_when_enabled(
        self, auth_enabled_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Without a session cookie the endpoint reports ``401``."""
        response = auth_enabled_client.post(self.ENDPOINT, json=valid_signal_payload())

        self.assert_unauthorized(response)
        self.assert_documented_status(api_spec, response)


class TestListDecisionSignals(BaseAPITest):
    """``GET /api/v1/decision-signals``."""

    ENDPOINT = "/api/v1/decision-signals"
    METHOD = "get"

    def test_returns_empty_page(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """No stored signals yields an empty page."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert self.assert_paginated(body, page=1) == []

    def test_lists_created_signals(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_signal: Callable[..., dict[str, Any]],
    ) -> None:
        """Created signals are returned by the listing."""
        signal = create_signal()

        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == 1
        assert body["items"][0]["id"] == signal["id"]

    @pytest.mark.parametrize(
        ("param", "matching", "non_matching"),
        [
            ("stock_code", "600519", "000858"),
            ("action", "buy", "sell"),
            ("source_type", "analysis", "agent"),
            ("status", "active", "closed"),
            ("trigger_source", "api-suite", "scheduler"),
        ],
    )
    def test_filters_narrow_the_listing(
        self,
        api_client: TestClient,
        create_signal: Callable[..., dict[str, Any]],
        param: str,
        matching: str,
        non_matching: str,
    ) -> None:
        """Each documented filter matches only the intended signals."""
        create_signal()

        hit = self.assert_ok(api_client.get(self.ENDPOINT, params={param: matching}))
        miss = self.assert_ok(api_client.get(self.ENDPOINT, params={param: non_matching}))

        assert hit["total"] == 1
        assert miss["total"] == 0

    def test_paginates_results(
        self, api_client: TestClient, create_signal: Callable[..., dict[str, Any]]
    ) -> None:
        """``page``/``page_size`` slice the listing."""
        create_signal(stock_code="600519")
        create_signal(stock_code="000858")

        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"page": 2, "page_size": 1}))

        assert body["total"] == 2
        assert body["page"] == 2
        assert len(body["items"]) == 1

    @pytest.mark.parametrize(
        ("field", "value"), [("page", 0), ("page_size", 0), ("page_size", 101)]
    )
    def test_rejects_invalid_pagination(
        self, api_client: TestClient, field: str, value: int
    ) -> None:
        """Pagination bounds documented in api_spec.json are enforced."""
        response = api_client.get(self.ENDPOINT, params={field: value})

        self.assert_validation_error(response, field=field)

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Without a session cookie the endpoint reports ``401``."""
        self.assert_unauthorized(auth_enabled_client.get(self.ENDPOINT))


class TestGetDecisionSignal(BaseAPITest):
    """``GET /api/v1/decision-signals/{signal_id}``."""

    ENDPOINT = "/api/v1/decision-signals/{signal_id}"
    METHOD = "get"

    def test_returns_signal_by_id(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_signal: Callable[..., dict[str, Any]],
    ) -> None:
        """An existing signal is returned in full."""
        signal = create_signal()

        response = api_client.get(f"/api/v1/decision-signals/{signal['id']}")

        body = self.assert_matches_spec(api_spec, response)
        assert body["id"] == signal["id"]
        assert body["stock_code"] == "600519"

    def test_returns_404_for_unknown_signal(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Unknown ids report a documented ``404``."""
        response = api_client.get("/api/v1/decision-signals/999999")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)

    def test_rejects_non_integer_signal_id(self, api_client: TestClient) -> None:
        """``signal_id`` must be an integer path parameter."""
        response = api_client.get("/api/v1/decision-signals/not-a-number")

        self.assert_validation_error(response, field="signal_id")


class TestLatestDecisionSignals(BaseAPITest):
    """``GET /api/v1/decision-signals/latest/{stock_code}``."""

    ENDPOINT = "/api/v1/decision-signals/latest/{stock_code}"
    METHOD = "get"

    def test_returns_empty_list_without_signals(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A stock without active signals returns an empty page, not ``404``."""
        response = api_client.get("/api/v1/decision-signals/latest/600519")

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == 0

    def test_returns_latest_active_signal(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_signal: Callable[..., dict[str, Any]],
    ) -> None:
        """Only the requested stock's active signals are returned."""
        signal = create_signal()
        create_signal(stock_code="000858", trigger_source="other")

        response = api_client.get("/api/v1/decision-signals/latest/600519")

        body = self.assert_matches_spec(api_spec, response)
        assert [item["id"] for item in body["items"]] == [signal["id"]]

    @pytest.mark.parametrize("limit", [0, 101])
    def test_rejects_out_of_range_limit(self, api_client: TestClient, limit: int) -> None:
        """``limit`` honors the documented 1..100 range."""
        response = api_client.get("/api/v1/decision-signals/latest/600519", params={"limit": limit})

        self.assert_validation_error(response, field="limit")


class TestUpdateDecisionSignalStatus(BaseAPITest):
    """``PATCH /api/v1/decision-signals/{signal_id}/status``."""

    ENDPOINT = "/api/v1/decision-signals/{signal_id}/status"
    METHOD = "patch"

    def test_updates_status(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_signal: Callable[..., dict[str, Any]],
    ) -> None:
        """A documented status transition is persisted."""
        signal = create_signal()

        response = api_client.patch(
            f"/api/v1/decision-signals/{signal['id']}/status", json={"status": "closed"}
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["id"] == signal["id"]
        assert body["status"] == "closed"

    def test_rejects_unknown_status(
        self, api_client: TestClient, create_signal: Callable[..., dict[str, Any]]
    ) -> None:
        """``status`` is restricted to the documented enumeration."""
        signal = create_signal()

        response = api_client.patch(
            f"/api/v1/decision-signals/{signal['id']}/status", json={"status": "paused"}
        )

        self.assert_validation_error(response, field="status")

    def test_returns_404_for_unknown_signal(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Unknown ids report a documented ``404``."""
        response = api_client.patch(
            "/api/v1/decision-signals/999999/status", json={"status": "closed"}
        )

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)


class TestDecisionSignalFeedback(BaseAPITest):
    """``GET``/``PUT`` ``/api/v1/decision-signals/{signal_id}/feedback``."""

    ENDPOINT = "/api/v1/decision-signals/{signal_id}/feedback"
    METHOD = "put"
    EXTRA_ENDPOINTS = (("/api/v1/decision-signals/{signal_id}/feedback", "get"),)

    def test_stores_and_reads_back_feedback(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_signal: Callable[..., dict[str, Any]],
    ) -> None:
        """Submitted feedback is persisted and readable."""
        signal = create_signal()
        payload = {"feedback_value": "useful", "reason_code": "actionable", "note": "清晰"}

        put_response = api_client.put(
            f"/api/v1/decision-signals/{signal['id']}/feedback", json=payload
        )

        body = self.assert_matches_spec(api_spec, put_response)
        assert body["signal_id"] == signal["id"]
        assert body["feedback_value"] == "useful"
        assert body["source"] == "api"

        get_body = self.assert_ok(
            api_client.get(f"/api/v1/decision-signals/{signal['id']}/feedback")
        )
        assert get_body["feedback_value"] == "useful"
        assert get_body["reason_code"] == "actionable"

    def test_overwrites_previous_feedback(
        self, api_client: TestClient, create_signal: Callable[..., dict[str, Any]]
    ) -> None:
        """A second submission replaces the stored value."""
        signal = create_signal()
        url = f"/api/v1/decision-signals/{signal['id']}/feedback"

        self.assert_ok(api_client.put(url, json={"feedback_value": "useful"}))
        body = self.assert_ok(api_client.put(url, json={"feedback_value": "not_useful"}))

        assert body["feedback_value"] == "not_useful"

    def test_get_returns_empty_feedback_before_submission(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_signal: Callable[..., dict[str, Any]],
    ) -> None:
        """Reading feedback that was never submitted returns a null value."""
        signal = create_signal()

        response = api_client.get(f"/api/v1/decision-signals/{signal['id']}/feedback")

        body = self.assert_matches_spec(api_spec, response)
        assert body["signal_id"] == signal["id"]
        assert body["feedback_value"] is None

    @pytest.mark.parametrize("feedback_value", ["great", "", None])
    def test_rejects_unknown_feedback_value(
        self,
        api_client: TestClient,
        create_signal: Callable[..., dict[str, Any]],
        feedback_value: Any,
    ) -> None:
        """``feedback_value`` is restricted to the documented enumeration."""
        signal = create_signal()

        response = api_client.put(
            f"/api/v1/decision-signals/{signal['id']}/feedback",
            json={"feedback_value": feedback_value},
        )

        self.assert_validation_error(response, field="feedback_value")

    def test_returns_404_for_unknown_signal(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Feedback for a missing signal reports a documented ``404``."""
        response = api_client.put(
            "/api/v1/decision-signals/999999/feedback", json={"feedback_value": "useful"}
        )

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)
