"""API tests for the admin authentication endpoints.

The suite environment starts with ``ADMIN_AUTH_ENABLED=false`` and no stored
password, so these tests drive the full enable/login/change/disable lifecycle
against the isolated temporary ``.env`` created by the package ``conftest``.
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api

PASSWORD = "Str0ng-Suite-Pass!"
NEW_PASSWORD = "Even-Str0nger-Pass!"


def enable_auth(client: TestClient, password: str = PASSWORD) -> None:
    """Turn on password login by setting an initial admin password."""
    response = client.post(
        "/api/v1/auth/settings",
        json={"authEnabled": True, "password": password, "passwordConfirm": password},
    )
    assert response.status_code == 200, response.text


class TestAuthStatus(BaseAPITest):
    """``GET /api/v1/auth/status``."""

    ENDPOINT = "/api/v1/auth/status"
    METHOD = "get"

    def test_reports_disabled_state_without_setup(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A fresh installation reports no password and no session."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["authEnabled"] is False
        assert body["loggedIn"] is False
        assert body["passwordSet"] is False
        assert body["setupState"] == "no_password"

    def test_reports_enabled_state_after_setup(self, api_client: TestClient) -> None:
        """After enabling auth the status reflects the active session."""
        enable_auth(api_client)

        body = self.assert_ok(api_client.get(self.ENDPOINT))

        assert body["authEnabled"] is True
        assert body["passwordSet"] is True
        assert body["loggedIn"] is True
        assert body["setupState"] == "enabled"

    def test_is_reachable_without_a_session(self, auth_enabled_client: TestClient) -> None:
        """The status endpoint is exempt from the auth middleware."""
        body = self.assert_ok(auth_enabled_client.get(self.ENDPOINT))

        assert body["loggedIn"] is False


class TestAuthSettings(BaseAPITest):
    """``POST /api/v1/auth/settings``."""

    ENDPOINT = "/api/v1/auth/settings"
    METHOD = "post"

    def test_enables_auth_and_opens_a_session(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Enabling auth stores the password and issues a session cookie."""
        response = api_client.post(
            self.ENDPOINT,
            json={"authEnabled": True, "password": PASSWORD, "passwordConfirm": PASSWORD},
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["authEnabled"] is True
        assert body["loggedIn"] is True
        assert "dsa_session" in response.cookies or response.headers.get("set-cookie")

    def test_rejects_mismatched_confirmation(self, api_client: TestClient) -> None:
        """``password`` and ``passwordConfirm`` must agree."""
        response = api_client.post(
            self.ENDPOINT,
            json={"authEnabled": True, "password": PASSWORD, "passwordConfirm": "different"},
        )

        self.assert_error(response, 400, "password_mismatch")

    def test_rejects_enabling_without_a_password(self, api_client: TestClient) -> None:
        """Auth cannot be enabled before a password exists."""
        response = api_client.post(self.ENDPOINT, json={"authEnabled": True})

        self.assert_error(response, 400, "password_required")

    def test_rejects_resetting_an_existing_password(self, api_client: TestClient) -> None:
        """A stored password may only be replaced through change-password."""
        enable_auth(api_client)

        response = api_client.post(
            self.ENDPOINT,
            json={"authEnabled": True, "password": NEW_PASSWORD, "passwordConfirm": NEW_PASSWORD},
        )

        self.assert_error(response, 400, "password_already_set")

    def test_disables_auth_with_an_active_session(self, api_client: TestClient) -> None:
        """A logged-in admin can switch password login back off."""
        enable_auth(api_client)

        body = self.assert_ok(api_client.post(self.ENDPOINT, json={"authEnabled": False}))

        assert body["authEnabled"] is False
        assert body["setupState"] == "password_retained"

    def test_rejects_missing_auth_enabled_flag(self, api_client: TestClient) -> None:
        """``authEnabled`` is a required body field."""
        response = api_client.post(self.ENDPOINT, json={})

        self.assert_validation_error(response, field="authEnabled")


class TestAuthLogin(BaseAPITest):
    """``POST /api/v1/auth/login``."""

    ENDPOINT = "/api/v1/auth/login"
    METHOD = "post"

    def test_rejects_login_while_auth_is_disabled(self, api_client: TestClient) -> None:
        """Without password login configured there is nothing to log into."""
        response = api_client.post(self.ENDPOINT, json={"password": PASSWORD})

        self.assert_error(response, 400, "auth_disabled")

    def test_rejects_empty_password(self, api_client: TestClient) -> None:
        """An empty password is rejected before any verification work."""
        enable_auth(api_client)

        response = api_client.post(self.ENDPOINT, json={"password": "   "})

        self.assert_error(response, 400, "password_required")

    def test_accepts_the_stored_password(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A correct password opens a new session."""
        enable_auth(api_client)
        api_client.cookies.clear()

        response = api_client.post(self.ENDPOINT, json={"password": PASSWORD})

        body = self.assert_matches_spec(api_spec, response)
        assert body == {"ok": True}

    def test_rejects_a_wrong_password(self, api_client: TestClient) -> None:
        """An incorrect password reports ``401``."""
        enable_auth(api_client)
        api_client.cookies.clear()

        response = api_client.post(self.ENDPOINT, json={"password": "wrong-password"})

        self.assert_error(response, 401, "invalid_password")

    def test_is_reachable_without_a_session(self, auth_enabled_client: TestClient) -> None:
        """The login endpoint is exempt from the auth middleware."""
        response = auth_enabled_client.post(self.ENDPOINT, json={"password": ""})

        assert response.status_code != 401


class TestAuthChangePassword(BaseAPITest):
    """``POST /api/v1/auth/change-password``."""

    ENDPOINT = "/api/v1/auth/change-password"
    METHOD = "post"

    def test_changes_the_stored_password(self, api_client: TestClient) -> None:
        """A valid change returns ``204`` and the new password then works."""
        enable_auth(api_client)

        response = api_client.post(
            self.ENDPOINT,
            json={
                "currentPassword": PASSWORD,
                "newPassword": NEW_PASSWORD,
                "newPasswordConfirm": NEW_PASSWORD,
            },
        )

        assert response.status_code == 204, response.text
        api_client.cookies.clear()
        assert api_client.post("/api/v1/auth/login", json={"password": NEW_PASSWORD}).status_code == 200

    def test_rejects_missing_current_password(self, api_client: TestClient) -> None:
        """``currentPassword`` must be supplied."""
        enable_auth(api_client)

        response = api_client.post(
            self.ENDPOINT,
            json={"newPassword": NEW_PASSWORD, "newPasswordConfirm": NEW_PASSWORD},
        )

        self.assert_error(response, 400, "current_required")

    def test_rejects_mismatched_confirmation(self, api_client: TestClient) -> None:
        """The new password and its confirmation must agree."""
        enable_auth(api_client)

        response = api_client.post(
            self.ENDPOINT,
            json={
                "currentPassword": PASSWORD,
                "newPassword": NEW_PASSWORD,
                "newPasswordConfirm": "different",
            },
        )

        self.assert_error(response, 400, "password_mismatch")

    def test_rejects_a_wrong_current_password(self, api_client: TestClient) -> None:
        """The current password is verified before any change is stored."""
        enable_auth(api_client)

        response = api_client.post(
            self.ENDPOINT,
            json={
                "currentPassword": "wrong-password",
                "newPassword": NEW_PASSWORD,
                "newPasswordConfirm": NEW_PASSWORD,
            },
        )

        self.assert_error(response, 400, "invalid_password")

    def test_rejects_change_when_no_password_exists(self, api_client: TestClient) -> None:
        """Without password login configured there is nothing to change."""
        response = api_client.post(
            self.ENDPOINT,
            json={
                "currentPassword": PASSWORD,
                "newPassword": NEW_PASSWORD,
                "newPasswordConfirm": NEW_PASSWORD,
            },
        )

        self.assert_error(response, 400, "not_changeable")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """This endpoint is not exempt from the auth middleware."""
        response = auth_enabled_client.post(
            self.ENDPOINT,
            json={
                "currentPassword": PASSWORD,
                "newPassword": NEW_PASSWORD,
                "newPasswordConfirm": NEW_PASSWORD,
            },
        )

        self.assert_unauthorized(response)


class TestAuthLogout(BaseAPITest):
    """``POST /api/v1/auth/logout``."""

    ENDPOINT = "/api/v1/auth/logout"
    METHOD = "post"

    def test_clears_the_session(self, api_client: TestClient) -> None:
        """Logging out returns ``204`` and ends the session."""
        enable_auth(api_client)

        response = api_client.post(self.ENDPOINT)

        assert response.status_code == 204, response.text
        assert self.assert_ok(api_client.get("/api/v1/auth/status"))["loggedIn"] is False

    def test_is_a_no_op_when_auth_is_disabled(self, api_client: TestClient) -> None:
        """Logging out without an active session still succeeds."""
        response = api_client.post(self.ENDPOINT)

        assert response.status_code == 204, response.text
