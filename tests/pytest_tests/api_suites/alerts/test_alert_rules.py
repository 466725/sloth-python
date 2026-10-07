"""API tests for the alert rule management endpoints."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api


def valid_rule_payload(**overrides: Any) -> dict[str, Any]:
    """Return the smallest payload the alert service accepts."""
    payload: dict[str, Any] = {
        "name": "茅台上涨提醒",
        "target_scope": "single_symbol",
        "target": "600519",
        "alert_type": "price_change_percent",
        "parameters": {"direction": "up", "change_pct": 3.0},
        "severity": "warning",
        "enabled": True,
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def create_rule(api_client: TestClient) -> Callable[..., dict[str, Any]]:
    """Create an alert rule and return the stored representation."""

    def _create(**overrides: Any) -> dict[str, Any]:
        response = api_client.post("/api/v1/alerts/rules", json=valid_rule_payload(**overrides))
        assert response.status_code == 200, response.text
        return response.json()

    return _create


class TestCreateAlertRule(BaseAPITest):
    """``POST /api/v1/alerts/rules``."""

    ENDPOINT = "/api/v1/alerts/rules"
    METHOD = "post"

    def test_creates_rule_with_normalized_parameters(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A valid payload is persisted and echoed back with an id."""
        response = api_client.post(self.ENDPOINT, json=valid_rule_payload())

        body = self.assert_matches_spec(api_spec, response)
        assert body["id"] > 0
        assert body["target"] == "600519"
        assert body["alert_type"] == "price_change_percent"
        assert body["parameters"] == {"direction": "up", "change_pct": 3.0}
        assert body["enabled"] is True

    def test_applies_documented_defaults(self, api_client: TestClient) -> None:
        """Omitted optional fields fall back to the documented defaults."""
        payload = {
            "target": "600519",
            "alert_type": "price_change_percent",
            "parameters": {"change_pct": 2},
        }

        body = self.assert_ok(api_client.post(self.ENDPOINT, json=payload))

        assert body["target_scope"] == "single_symbol"
        assert body["severity"] == "warning"
        assert body["enabled"] is True
        assert body["parameters"]["direction"] == "up"

    @pytest.mark.parametrize(
        ("overrides", "field"),
        [
            ({"alert_type": "volume_spike"}, "alert_type"),
            ({"target_scope": "sector"}, "target_scope"),
            ({"severity": "fatal"}, "severity"),
            ({"target": ""}, "target"),
            ({"target": "x" * 65}, "target"),
        ],
    )
    def test_rejects_values_outside_the_schema(
        self, api_client: TestClient, overrides: dict[str, Any], field: str
    ) -> None:
        """Enumerations and length limits are enforced by the request model."""
        response = api_client.post(self.ENDPOINT, json=valid_rule_payload(**overrides))

        self.assert_validation_error(response, field=field)

    def test_rejects_missing_required_fields(self, api_client: TestClient) -> None:
        """``target`` and ``alert_type`` are required."""
        response = api_client.post(self.ENDPOINT, json={})

        body = self.assert_validation_error(response)
        missing = {entry["loc"][-1] for entry in body["detail"]}
        assert {"target", "alert_type"} <= missing

    @pytest.mark.parametrize(
        "parameters",
        [
            {"direction": "sideways", "change_pct": 3},
            {"direction": "up", "change_pct": 0},
            {"direction": "up", "change_pct": -5},
            {"direction": "up", "change_pct": "abc"},
            {"direction": "up"},
        ],
    )
    def test_rejects_invalid_alert_parameters(
        self, api_client: TestClient, api_spec: dict[str, Any], parameters: dict[str, Any]
    ) -> None:
        """Service-level parameter validation surfaces as ``400``."""
        response = api_client.post(self.ENDPOINT, json=valid_rule_payload(parameters=parameters))

        self.assert_error(response, 400, "validation_error")
        self.assert_documented_status(api_spec, response)


class TestListAlertRules(BaseAPITest):
    """``GET /api/v1/alerts/rules``."""

    ENDPOINT = "/api/v1/alerts/rules"
    METHOD = "get"

    def test_returns_empty_page(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """No configured rules yields an empty page."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert self.assert_paginated(body, page=1) == []

    def test_lists_created_rules(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_rule: Callable[..., dict[str, Any]],
    ) -> None:
        """Created rules appear in the listing."""
        rule = create_rule()

        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["total"] == 1
        assert body["items"][0]["id"] == rule["id"]

    def test_filters_by_enabled_flag(
        self, api_client: TestClient, create_rule: Callable[..., dict[str, Any]]
    ) -> None:
        """``enabled`` selects only rules in the requested state."""
        create_rule(target="600519")
        create_rule(target="000858", enabled=False)

        enabled = self.assert_ok(api_client.get(self.ENDPOINT, params={"enabled": "true"}))
        disabled = self.assert_ok(api_client.get(self.ENDPOINT, params={"enabled": "false"}))

        assert [item["target"] for item in enabled["items"]] == ["600519"]
        assert [item["target"] for item in disabled["items"]] == ["000858"]

    def test_filters_by_target(
        self, api_client: TestClient, create_rule: Callable[..., dict[str, Any]]
    ) -> None:
        """``target`` narrows the listing to a single symbol."""
        create_rule(target="600519")
        create_rule(target="000858")

        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"target": "000858"}))

        assert body["total"] == 1
        assert body["items"][0]["target"] == "000858"

    def test_paginates_results(
        self, api_client: TestClient, create_rule: Callable[..., dict[str, Any]]
    ) -> None:
        """``page``/``page_size`` slice the listing."""
        create_rule(target="600519")
        create_rule(target="000858")

        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"page": 2, "page_size": 1}))

        assert body["total"] == 2
        assert body["page"] == 2
        assert len(body["items"]) == 1

    @pytest.mark.parametrize(
        ("field", "value"),
        [("page", 0), ("page_size", 0), ("page_size", 101), ("alert_type", "volume_spike")],
    )
    def test_rejects_invalid_query_parameters(
        self, api_client: TestClient, field: str, value: Any
    ) -> None:
        """Query bounds and enumerations documented in api_spec.json are enforced."""
        response = api_client.get(self.ENDPOINT, params={field: value})

        self.assert_validation_error(response, field=field)


class TestGetAlertRule(BaseAPITest):
    """``GET /api/v1/alerts/rules/{rule_id}``."""

    ENDPOINT = "/api/v1/alerts/rules/{rule_id}"
    METHOD = "get"

    def test_returns_rule_by_id(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_rule: Callable[..., dict[str, Any]],
    ) -> None:
        """An existing rule is returned in full."""
        rule = create_rule()

        response = api_client.get(f"/api/v1/alerts/rules/{rule['id']}")

        body = self.assert_matches_spec(api_spec, response)
        assert body == rule

    def test_returns_404_for_unknown_rule(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Unknown ids report a documented ``404``."""
        response = api_client.get("/api/v1/alerts/rules/999999")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)

    def test_rejects_non_integer_rule_id(self, api_client: TestClient) -> None:
        """``rule_id`` must be an integer path parameter."""
        response = api_client.get("/api/v1/alerts/rules/not-a-number")

        self.assert_validation_error(response, field="rule_id")


class TestUpdateAlertRule(BaseAPITest):
    """``PATCH /api/v1/alerts/rules/{rule_id}``."""

    ENDPOINT = "/api/v1/alerts/rules/{rule_id}"
    METHOD = "patch"

    def test_updates_only_supplied_fields(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_rule: Callable[..., dict[str, Any]],
    ) -> None:
        """A partial payload leaves untouched fields unchanged."""
        rule = create_rule()

        response = api_client.patch(
            f"/api/v1/alerts/rules/{rule['id']}", json={"severity": "critical"}
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["severity"] == "critical"
        assert body["target"] == rule["target"]
        assert body["parameters"] == rule["parameters"]

    def test_rejects_empty_payload(
        self, api_client: TestClient, create_rule: Callable[..., dict[str, Any]]
    ) -> None:
        """An update must change at least one field."""
        rule = create_rule()

        response = api_client.patch(f"/api/v1/alerts/rules/{rule['id']}", json={})

        self.assert_error(response, 400, "validation_error")

    def test_returns_404_for_unknown_rule(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Updating a missing rule reports a documented ``404``."""
        response = api_client.patch("/api/v1/alerts/rules/999999", json={"severity": "info"})

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)

    def test_rejects_invalid_parameters(
        self, api_client: TestClient, create_rule: Callable[..., dict[str, Any]]
    ) -> None:
        """Parameter validation also applies to updates."""
        rule = create_rule()

        response = api_client.patch(
            f"/api/v1/alerts/rules/{rule['id']}",
            json={"parameters": {"direction": "sideways", "change_pct": 1}},
        )

        self.assert_error(response, 400, "validation_error")


class TestDeleteAlertRule(BaseAPITest):
    """``DELETE /api/v1/alerts/rules/{rule_id}``."""

    ENDPOINT = "/api/v1/alerts/rules/{rule_id}"
    METHOD = "delete"

    def test_deletes_existing_rule(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_rule: Callable[..., dict[str, Any]],
    ) -> None:
        """Deleting a rule reports one removal and empties the listing."""
        rule = create_rule()

        response = api_client.delete(f"/api/v1/alerts/rules/{rule['id']}")

        body = self.assert_matches_spec(api_spec, response)
        assert body == {"deleted": 1}
        assert self.assert_ok(api_client.get("/api/v1/alerts/rules"))["total"] == 0

    def test_returns_404_for_unknown_rule(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Deleting a missing rule reports a documented ``404``."""
        response = api_client.delete("/api/v1/alerts/rules/999999")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)


class TestEnableAlertRule(BaseAPITest):
    """``POST /api/v1/alerts/rules/{rule_id}/enable``."""

    ENDPOINT = "/api/v1/alerts/rules/{rule_id}/enable"
    METHOD = "post"

    def test_enables_disabled_rule(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_rule: Callable[..., dict[str, Any]],
    ) -> None:
        """A disabled rule becomes enabled."""
        rule = create_rule(enabled=False)

        response = api_client.post(f"/api/v1/alerts/rules/{rule['id']}/enable")

        body = self.assert_matches_spec(api_spec, response)
        assert body["enabled"] is True

    def test_enabling_twice_is_idempotent(
        self, api_client: TestClient, create_rule: Callable[..., dict[str, Any]]
    ) -> None:
        """Enabling an already enabled rule keeps it enabled."""
        rule = create_rule(enabled=True)

        body = self.assert_ok(api_client.post(f"/api/v1/alerts/rules/{rule['id']}/enable"))

        assert body["enabled"] is True

    def test_returns_404_for_unknown_rule(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Unknown ids report a documented ``404``."""
        response = api_client.post("/api/v1/alerts/rules/999999/enable")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)


class TestDisableAlertRule(BaseAPITest):
    """``POST /api/v1/alerts/rules/{rule_id}/disable``."""

    ENDPOINT = "/api/v1/alerts/rules/{rule_id}/disable"
    METHOD = "post"

    def test_disables_enabled_rule(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_rule: Callable[..., dict[str, Any]],
    ) -> None:
        """An enabled rule becomes disabled."""
        rule = create_rule(enabled=True)

        response = api_client.post(f"/api/v1/alerts/rules/{rule['id']}/disable")

        body = self.assert_matches_spec(api_spec, response)
        assert body["enabled"] is False

    def test_returns_404_for_unknown_rule(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Unknown ids report a documented ``404``."""
        response = api_client.post("/api/v1/alerts/rules/999999/disable")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)


class TestAlertRuleDryRun(BaseAPITest):
    """``POST /api/v1/alerts/rules/{rule_id}/test``."""

    ENDPOINT = "/api/v1/alerts/rules/{rule_id}/test"
    METHOD = "post"

    def test_returns_dry_run_result(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        create_rule: Callable[..., dict[str, Any]],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """The dry run reports an evaluation outcome without sending notifications."""
        from ai_stock.services.alert_service import AlertService

        rule = create_rule()
        monkeypatch.setattr(
            AlertService,
            "test_rule",
            lambda self, rule_id: {
                "rule_id": rule_id,
                "target_scope": "single_symbol",
                "status": "not_triggered",
                "triggered": False,
                "observed_value": 1.2,
                "message": "current change 1.20% below threshold",
                "evaluated_count": 1,
            },
        )

        response = api_client.post(f"/api/v1/alerts/rules/{rule['id']}/test")

        body = self.assert_matches_spec(api_spec, response)
        assert body["rule_id"] == rule["id"]
        assert body["triggered"] is False
        assert body["status"] == "not_triggered"

    def test_returns_404_for_unknown_rule(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A missing rule is rejected before any market data is fetched."""
        response = api_client.post("/api/v1/alerts/rules/999999/test")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)
