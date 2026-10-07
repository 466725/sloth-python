"""API tests for the system configuration endpoints.

All tests run against the throwaway ``.env`` created by the package
``conftest``; configuration writes therefore never touch the developer's real
settings. Connectivity tests (LLM channel, notification channel, model
discovery) are exercised with deliberately incomplete configuration so the
service short-circuits before any outbound request.
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api

PASSWORD = "Str0ng-Suite-Pass!"


def current_version(client: TestClient) -> str:
    """Return the current optimistic-concurrency token for the config file."""
    response = client.get("/api/v1/system/config")
    assert response.status_code == 200, response.text
    return response.json()["config_version"]


def enable_auth(client: TestClient) -> None:
    """Enable password login so env backup access is permitted."""
    response = client.post(
        "/api/v1/auth/settings",
        json={"authEnabled": True, "password": PASSWORD, "passwordConfirm": PASSWORD},
    )
    assert response.status_code == 200, response.text


class TestGetSystemConfig(BaseAPITest):
    """``GET /api/v1/system/config``."""

    ENDPOINT = "/api/v1/system/config"
    METHOD = "get"

    def test_returns_values_with_schema_metadata(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """The default read includes field metadata for form rendering."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["config_version"]
        assert body["mask_token"]
        assert body["items"]
        assert any(item["schema"] for item in body["items"])

    def test_exposes_the_configured_watchlist(self, api_client: TestClient) -> None:
        """Values come from the isolated ``.env`` rather than the real one."""
        body = self.assert_ok(api_client.get(self.ENDPOINT))
        items = {item["key"]: item for item in body["items"]}

        assert items["STOCK_LIST"]["value"] == "600519,000858"
        assert items["STOCK_LIST"]["raw_value_exists"] is True
        assert items["STOCK_LIST"]["is_masked"] is False

    def test_omits_schema_when_not_requested(self, api_client: TestClient) -> None:
        """``include_schema=false`` returns a lighter payload."""
        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"include_schema": "false"}))

        assert all(item["schema"] is None for item in body["items"])

    def test_rejects_a_non_boolean_include_schema(self, api_client: TestClient) -> None:
        """``include_schema`` must be parseable as a boolean."""
        response = api_client.get(self.ENDPOINT, params={"include_schema": "maybe"})

        self.assert_validation_error(response, field="include_schema")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Configuration is only readable by an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.get(self.ENDPOINT))


class TestGetSetupStatus(BaseAPITest):
    """``GET /api/v1/system/config/setup/status``."""

    ENDPOINT = "/api/v1/system/config/setup/status"
    METHOD = "get"

    def test_reports_outstanding_first_run_steps(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A credential-free environment is reported as incomplete."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["is_complete"] is False
        assert "llm_primary" in body["required_missing_keys"]
        assert body["next_step_key"] in body["required_missing_keys"]

    def test_describes_every_readiness_check(self, api_client: TestClient) -> None:
        """Each check carries the metadata the setup wizard renders."""
        body = self.assert_ok(api_client.get(self.ENDPOINT))

        assert body["checks"]
        for check in body["checks"]:
            assert check["key"]
            assert check["category"] in {"base", "ai_model", "agent", "notification", "system"}
            assert check["status"] in {"configured", "inherited", "optional", "needs_action"}

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Setup status is only readable by an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.get(self.ENDPOINT))


class TestGetSystemConfigSchema(BaseAPITest):
    """``GET /api/v1/system/config/schema``."""

    ENDPOINT = "/api/v1/system/config/schema"
    METHOD = "get"

    def test_returns_categorised_field_metadata(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """The schema groups every editable field under a category."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["schema_version"]
        assert body["categories"]
        assert all(category["title"] for category in body["categories"])
        assert any(category["fields"] for category in body["categories"])

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """The schema is only readable by an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.get(self.ENDPOINT))


class TestUpdateSystemConfig(BaseAPITest):
    """``PUT /api/v1/system/config``."""

    ENDPOINT = "/api/v1/system/config"
    METHOD = "put"

    def test_persists_the_submitted_values(
        self, api_client: TestClient, api_spec: dict[str, Any], api_env
    ) -> None:
        """A valid update writes the key to the isolated ``.env``."""
        response = api_client.put(
            self.ENDPOINT,
            json={
                "config_version": current_version(api_client),
                "reload_now": False,
                "items": [{"key": "STOCK_LIST", "value": "600519,000001"}],
            },
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["success"] is True
        assert body["applied_count"] == 1
        assert body["updated_keys"] == ["STOCK_LIST"]
        assert body["reload_triggered"] is False
        assert api_env.read_env()["STOCK_LIST"] == "600519,000001"

    def test_rotates_the_config_version(self, api_client: TestClient) -> None:
        """Each successful write invalidates the previous version token."""
        version = current_version(api_client)

        body = self.assert_ok(
            api_client.put(
                self.ENDPOINT,
                json={
                    "config_version": version,
                    "reload_now": False,
                    "items": [{"key": "STOCK_LIST", "value": "600519"}],
                },
            )
        )

        assert body["config_version"] != version

    def test_rejects_a_stale_config_version(self, api_client: TestClient) -> None:
        """Concurrent edits are blocked with ``409``."""
        response = api_client.put(
            self.ENDPOINT,
            json={
                "config_version": "stale-version",
                "reload_now": False,
                "items": [{"key": "STOCK_LIST", "value": "600519"}],
            },
        )

        body = self.assert_error(response, 409, "config_version_conflict")
        assert body["current_config_version"]

    def test_rejects_a_value_outside_the_allowed_options(self, api_client: TestClient) -> None:
        """Enum-backed fields are validated before anything is written."""
        response = api_client.put(
            self.ENDPOINT,
            json={
                "config_version": current_version(api_client),
                "reload_now": False,
                "items": [{"key": "REPORT_LANGUAGE", "value": "xx"}],
            },
        )

        body = self.assert_error(response, 400, "validation_failed")
        assert body["issues"][0]["key"] == "REPORT_LANGUAGE"
        assert body["issues"][0]["code"] == "invalid_enum"
        assert body["issues"][0]["severity"] == "error"

    def test_rejects_an_empty_item_list(self, api_client: TestClient) -> None:
        """At least one key/value pair must be supplied."""
        response = api_client.put(
            self.ENDPOINT,
            json={"config_version": current_version(api_client), "items": []},
        )

        self.assert_validation_error(response, field="items")

    def test_rejects_a_missing_config_version(self, api_client: TestClient) -> None:
        """``config_version`` is required for optimistic concurrency."""
        response = api_client.put(
            self.ENDPOINT,
            json={"items": [{"key": "STOCK_LIST", "value": "600519"}]},
        )

        self.assert_validation_error(response, field="config_version")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Configuration writes are only allowed for an authenticated admin."""
        response = auth_enabled_client.put(
            self.ENDPOINT,
            json={"config_version": "any", "items": [{"key": "STOCK_LIST", "value": "600519"}]},
        )

        self.assert_unauthorized(response)


class TestValidateSystemConfig(BaseAPITest):
    """``POST /api/v1/system/config/validate``."""

    ENDPOINT = "/api/v1/system/config/validate"
    METHOD = "post"

    def test_accepts_valid_values(
        self, api_client: TestClient, api_spec: dict[str, Any], api_env
    ) -> None:
        """Validation reports success without writing to ``.env``."""
        response = api_client.post(
            self.ENDPOINT, json={"items": [{"key": "REPORT_LANGUAGE", "value": "en"}]}
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["valid"] is True
        assert body["issues"] == []
        assert api_env.read_env()["REPORT_LANGUAGE"] == "zh"

    def test_reports_values_outside_the_allowed_options(self, api_client: TestClient) -> None:
        """Invalid values are reported as issues rather than as an error status."""
        body = self.assert_ok(
            api_client.post(
                self.ENDPOINT, json={"items": [{"key": "REPORT_LANGUAGE", "value": "xx"}]}
            )
        )

        assert body["valid"] is False
        assert body["issues"][0]["key"] == "REPORT_LANGUAGE"
        assert body["issues"][0]["expected"] == "zh,en"
        assert body["issues"][0]["actual"] == "xx"

    def test_rejects_an_empty_item_list(self, api_client: TestClient) -> None:
        """At least one key/value pair must be supplied."""
        response = api_client.post(self.ENDPOINT, json={"items": []})

        self.assert_validation_error(response, field="items")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Validation is only available to an authenticated admin."""
        response = auth_enabled_client.post(
            self.ENDPOINT, json={"items": [{"key": "REPORT_LANGUAGE", "value": "en"}]}
        )

        self.assert_unauthorized(response)


class TestExportSystemConfig(BaseAPITest):
    """``GET /api/v1/system/config/export``."""

    ENDPOINT = "/api/v1/system/config/export"
    METHOD = "get"

    def test_returns_the_raw_env_in_desktop_mode(
        self, api_client: TestClient, api_spec: dict[str, Any], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The desktop runtime may read the backup without a session."""
        monkeypatch.setenv("DSA_DESKTOP_MODE", "true")

        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert "STOCK_LIST=600519,000858" in body["content"]
        assert body["config_version"]

    def test_returns_the_raw_env_for_an_authenticated_admin(self, api_client: TestClient) -> None:
        """A logged-in admin on a server deployment may download the backup."""
        enable_auth(api_client)

        body = self.assert_ok(api_client.get(self.ENDPOINT))

        assert "STOCK_LIST=600519,000858" in body["content"]

    def test_is_denied_while_admin_auth_is_disabled(self, api_client: TestClient) -> None:
        """Backups stay locked until password login is configured."""
        response = api_client.get(self.ENDPOINT)

        self.assert_error(response, 403, "env_backup_access_denied")

    def test_is_denied_without_a_session(self, api_client: TestClient) -> None:
        """An enabled deployment still requires a valid admin cookie."""
        enable_auth(api_client)
        api_client.cookies.clear()

        response = api_client.get(self.ENDPOINT)

        self.assert_unauthorized(response)


class TestImportSystemConfig(BaseAPITest):
    """``POST /api/v1/system/config/import``."""

    ENDPOINT = "/api/v1/system/config/import"
    METHOD = "post"

    def test_merges_the_backup_into_the_saved_config(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        api_env,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Imported keys are written to the active ``.env``."""
        monkeypatch.setenv("DSA_DESKTOP_MODE", "true")

        response = api_client.post(
            self.ENDPOINT,
            json={
                "config_version": current_version(api_client),
                "content": "STOCK_LIST=600519\nREPORT_LANGUAGE=en\n",
                "reload_now": False,
            },
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["success"] is True
        assert set(body["updated_keys"]) == {"STOCK_LIST", "REPORT_LANGUAGE"}
        assert api_env.read_env()["REPORT_LANGUAGE"] == "en"

    def test_rejects_a_stale_config_version(
        self, api_client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Imports use the same optimistic concurrency guard as updates."""
        monkeypatch.setenv("DSA_DESKTOP_MODE", "true")

        response = api_client.post(
            self.ENDPOINT,
            json={
                "config_version": "stale-version",
                "content": "STOCK_LIST=600519\n",
                "reload_now": False,
            },
        )

        body = self.assert_error(response, 409, "config_version_conflict")
        assert body["current_config_version"]

    def test_rejects_invalid_values_in_the_backup(
        self, api_client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Imported content is validated with the same rules as a manual update."""
        monkeypatch.setenv("DSA_DESKTOP_MODE", "true")

        response = api_client.post(
            self.ENDPOINT,
            json={
                "config_version": current_version(api_client),
                "content": "REPORT_LANGUAGE=xx\n",
                "reload_now": False,
            },
        )

        body = self.assert_error(response, 400, "validation_failed")
        assert body["issues"][0]["key"] == "REPORT_LANGUAGE"

    def test_rejects_missing_content(
        self, api_client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """``content`` is a required body field."""
        monkeypatch.setenv("DSA_DESKTOP_MODE", "true")

        response = api_client.post(
            self.ENDPOINT, json={"config_version": current_version(api_client)}
        )

        self.assert_validation_error(response, field="content")

    def test_is_denied_while_admin_auth_is_disabled(self, api_client: TestClient) -> None:
        """Restores stay locked until password login is configured."""
        response = api_client.post(
            self.ENDPOINT, json={"config_version": "any", "content": "STOCK_LIST=600519\n"}
        )

        self.assert_error(response, 403, "env_backup_access_denied")

    def test_is_denied_without_a_session(self, api_client: TestClient) -> None:
        """An enabled deployment still requires a valid admin cookie."""
        enable_auth(api_client)
        api_client.cookies.clear()

        response = api_client.post(
            self.ENDPOINT, json={"config_version": "any", "content": "STOCK_LIST=600519\n"}
        )

        self.assert_unauthorized(response)


class TestTestLLMChannel(BaseAPITest):
    """``POST /api/v1/system/config/llm/test-channel``."""

    ENDPOINT = "/api/v1/system/config/llm/test-channel"
    METHOD = "post"

    def test_reports_an_incomplete_channel_without_calling_out(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A channel without credentials fails during local validation."""
        response = api_client.post(
            self.ENDPOINT,
            json={"name": "suite", "protocol": "openai", "base_url": "", "api_key": ""},
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["success"] is False
        assert body["error_code"] == "invalid_config"
        assert body["retryable"] is False
        assert body["details"]["issue_code"] == "missing_api_key"

    def test_rejects_a_non_numeric_timeout(self, api_client: TestClient) -> None:
        """``timeout_seconds`` must be a number."""
        response = api_client.post(self.ENDPOINT, json={"name": "suite", "timeout_seconds": "soon"})

        self.assert_validation_error(response, field="timeout_seconds")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Channel tests are only available to an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.post(self.ENDPOINT, json={"name": "suite"}))


class TestTestNotificationChannel(BaseAPITest):
    """``POST /api/v1/system/config/notification/test-channel``."""

    ENDPOINT = "/api/v1/system/config/notification/test-channel"
    METHOD = "post"

    def test_reports_missing_channel_configuration(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """An unconfigured mail channel fails before any message is sent."""
        response = api_client.post(self.ENDPOINT, json={"channel": "email"})

        body = self.assert_matches_spec(api_spec, response)
        assert body["success"] is False
        assert body["error_code"] == "config_missing"
        assert body["stage"] == "config_validation"

    def test_rejects_an_unsupported_channel(self, api_client: TestClient) -> None:
        """Only the documented channels are accepted."""
        response = api_client.post(self.ENDPOINT, json={"channel": "sms"})

        self.assert_validation_error(response, field="channel")

    def test_rejects_an_empty_title(self, api_client: TestClient) -> None:
        """The test message title may not be blank."""
        response = api_client.post(self.ENDPOINT, json={"channel": "email", "title": ""})

        self.assert_validation_error(response, field="title")

    def test_rejects_a_timeout_below_the_minimum(self, api_client: TestClient) -> None:
        """``timeout_seconds`` is bounded to a sensible range."""
        response = api_client.post(self.ENDPOINT, json={"channel": "email", "timeout_seconds": 0.1})

        self.assert_validation_error(response, field="timeout_seconds")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Notification tests are only available to an authenticated admin."""
        response = auth_enabled_client.post(self.ENDPOINT, json={"channel": "email"})

        self.assert_unauthorized(response)


class TestDiscoverLLMChannelModels(BaseAPITest):
    """``POST /api/v1/system/config/llm/discover-models``."""

    ENDPOINT = "/api/v1/system/config/llm/discover-models"
    METHOD = "post"

    def test_reports_an_incomplete_channel_without_calling_out(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Discovery requires a base URL and fails locally without one."""
        response = api_client.post(
            self.ENDPOINT,
            json={"name": "suite", "protocol": "openai", "base_url": "", "api_key": "key"},
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["success"] is False
        assert body["error_code"] == "invalid_config"
        assert body["details"]["issue_code"] == "missing_base_url"
        assert body["models"] == []

    def test_rejects_a_non_numeric_timeout(self, api_client: TestClient) -> None:
        """``timeout_seconds`` must be a number."""
        response = api_client.post(self.ENDPOINT, json={"name": "suite", "timeout_seconds": "soon"})

        self.assert_validation_error(response, field="timeout_seconds")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Model discovery is only available to an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.post(self.ENDPOINT, json={"name": "suite"}))
