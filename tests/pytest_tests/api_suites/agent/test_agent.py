"""API tests for the AI agent endpoints.

The suite environment deliberately supplies no model credentials, so the agent
reports itself as unavailable and the conversational endpoints short-circuit
before any LLM request is attempted. Read-only endpoints are exercised against
the isolated SQLite database created by the package ``conftest``.
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api

AGENT_DISABLED_MESSAGE = "Agent mode is not enabled"


class TestGetAgentModels(BaseAPITest):
    """``GET /api/v1/agent/models``."""

    ENDPOINT = "/api/v1/agent/models"
    METHOD = "get"

    def test_returns_the_configured_deployments(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Without credentials the deployment list is empty but well formed."""
        response = api_client.get(self.ENDPOINT)

        self.assert_matches_spec(api_spec, response)

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Agent metadata is only readable by an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.get(self.ENDPOINT))


class TestGetAgentSkills(BaseAPITest):
    """``GET /api/v1/agent/skills``."""

    ENDPOINT = "/api/v1/agent/skills"
    METHOD = "get"

    def test_lists_the_user_invocable_skills(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Every advertised skill exposes an id, name and description."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["skills"]
        for skill in body["skills"]:
            assert skill["id"]
            assert skill["name"]
            assert isinstance(skill["description"], str)

    def test_nominates_a_default_skill(self, api_client: TestClient) -> None:
        """The default skill id refers to one of the listed skills."""
        body = self.assert_ok(api_client.get(self.ENDPOINT))

        assert body["default_skill_id"] in {skill["id"] for skill in body["skills"]}

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """The skill catalogue is only readable by an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.get(self.ENDPOINT))


class TestAgentChat(BaseAPITest):
    """``POST /api/v1/agent/chat``."""

    ENDPOINT = "/api/v1/agent/chat"
    METHOD = "post"

    def test_is_rejected_while_the_agent_is_unavailable(self, api_client: TestClient) -> None:
        """Chat requires a configured agent model."""
        response = api_client.post(self.ENDPOINT, json={"message": "你好"})

        body = self.assert_error(response, 400, "http_error")
        assert body["message"] == AGENT_DISABLED_MESSAGE

    def test_rejects_a_missing_message(self, api_client: TestClient) -> None:
        """``message`` is a required body field."""
        response = api_client.post(self.ENDPOINT, json={})

        self.assert_validation_error(response, field="message")

    def test_rejects_a_non_string_message(self, api_client: TestClient) -> None:
        """``message`` must be text."""
        response = api_client.post(self.ENDPOINT, json={"message": {"text": "hi"}})

        self.assert_validation_error(response, field="message")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Chat is only available to an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.post(self.ENDPOINT, json={"message": "hi"}))


class TestAgentChatStream(BaseAPITest):
    """``POST /api/v1/agent/chat/stream``."""

    ENDPOINT = "/api/v1/agent/chat/stream"
    METHOD = "post"

    def test_is_rejected_while_the_agent_is_unavailable(self, api_client: TestClient) -> None:
        """Streaming chat requires a configured agent model."""
        response = api_client.post(self.ENDPOINT, json={"message": "你好"})

        body = self.assert_error(response, 400, "http_error")
        assert body["message"] == AGENT_DISABLED_MESSAGE

    def test_rejects_a_missing_message(self, api_client: TestClient) -> None:
        """``message`` is a required body field."""
        response = api_client.post(self.ENDPOINT, json={})

        self.assert_validation_error(response, field="message")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Streaming chat is only available to an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.post(self.ENDPOINT, json={"message": "hi"}))


class TestAgentResearch(BaseAPITest):
    """``POST /api/v1/agent/research``."""

    ENDPOINT = "/api/v1/agent/research"
    METHOD = "post"

    def test_is_rejected_while_the_agent_is_unavailable(self, api_client: TestClient) -> None:
        """Deep research requires a configured agent model."""
        response = api_client.post(self.ENDPOINT, json={"question": "贵州茅台的护城河?"})

        body = self.assert_error(response, 400, "http_error")
        assert body["message"] == AGENT_DISABLED_MESSAGE

    def test_rejects_a_missing_question(self, api_client: TestClient) -> None:
        """``question`` is a required body field."""
        response = api_client.post(self.ENDPOINT, json={"stock_code": "600519"})

        self.assert_validation_error(response, field="question")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Deep research is only available to an authenticated admin."""
        response = auth_enabled_client.post(self.ENDPOINT, json={"question": "hi"})

        self.assert_unauthorized(response)


class TestListChatSessions(BaseAPITest):
    """``GET /api/v1/agent/chat/sessions``."""

    ENDPOINT = "/api/v1/agent/chat/sessions"
    METHOD = "get"

    def test_returns_an_empty_list_for_a_fresh_database(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """No conversations have been recorded yet."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["sessions"] == []

    def test_accepts_a_user_scope_filter(self, api_client: TestClient) -> None:
        """``user_id`` restricts results to one platform-prefixed owner."""
        body = self.assert_ok(
            api_client.get(self.ENDPOINT, params={"user_id": "telegram_12345", "limit": 5})
        )

        assert body["sessions"] == []

    def test_rejects_a_non_integer_limit(self, api_client: TestClient) -> None:
        """``limit`` must be an integer."""
        response = api_client.get(self.ENDPOINT, params={"limit": "many"})

        self.assert_validation_error(response, field="limit")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Session history is only readable by an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.get(self.ENDPOINT))


class TestGetChatSessionMessages(BaseAPITest):
    """``GET /api/v1/agent/chat/sessions/{session_id}``."""

    ENDPOINT = "/api/v1/agent/chat/sessions/{session_id}"
    METHOD = "get"

    def test_returns_an_empty_transcript_for_an_unknown_session(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Unknown sessions resolve to an empty message list."""
        response = api_client.get("/api/v1/agent/chat/sessions/missing-session")

        body = self.assert_matches_spec(api_spec, response)
        assert body["session_id"] == "missing-session"
        assert body["messages"] == []

    def test_rejects_a_non_integer_limit(self, api_client: TestClient) -> None:
        """``limit`` must be an integer."""
        response = api_client.get(
            "/api/v1/agent/chat/sessions/missing-session", params={"limit": "all"}
        )

        self.assert_validation_error(response, field="limit")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Transcripts are only readable by an authenticated admin."""
        self.assert_unauthorized(
            auth_enabled_client.get("/api/v1/agent/chat/sessions/missing-session")
        )


class TestDeleteChatSession(BaseAPITest):
    """``DELETE /api/v1/agent/chat/sessions/{session_id}``."""

    ENDPOINT = "/api/v1/agent/chat/sessions/{session_id}"
    METHOD = "delete"

    def test_reports_nothing_deleted_for_an_unknown_session(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Deleting a missing session is a successful no-op."""
        response = api_client.delete("/api/v1/agent/chat/sessions/missing-session")

        self.assert_documented_status(api_spec, response)
        assert response.json() == {"deleted": 0}

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Session deletion is only available to an authenticated admin."""
        self.assert_unauthorized(
            auth_enabled_client.delete("/api/v1/agent/chat/sessions/missing-session")
        )


class TestSendChatToNotification(BaseAPITest):
    """``POST /api/v1/agent/chat/send``."""

    ENDPOINT = "/api/v1/agent/chat/send"
    METHOD = "post"

    def test_reports_that_no_channel_is_configured(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Without notification channels the send is refused, not attempted."""
        response = api_client.post(self.ENDPOINT, json={"content": "今日复盘摘要"})

        self.assert_documented_status(api_spec, response)
        body = response.json()
        assert body["success"] is False
        assert body["error"] == "no_channels"

    def test_rejects_empty_content(self, api_client: TestClient) -> None:
        """``content`` must carry at least one character."""
        response = api_client.post(self.ENDPOINT, json={"content": ""})

        self.assert_validation_error(response, field="content")

    def test_rejects_content_above_the_size_limit(self, api_client: TestClient) -> None:
        """``content`` is capped to keep notification payloads deliverable."""
        response = api_client.post(self.ENDPOINT, json={"content": "x" * 50_001})

        self.assert_validation_error(response, field="content")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Sending to notification channels requires an authenticated admin."""
        response = auth_enabled_client.post(self.ENDPOINT, json={"content": "hi"})

        self.assert_unauthorized(response)
