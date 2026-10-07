"""API tests for the stock analysis endpoints.

Analysis submission is verified against a stubbed task queue (see the package
``conftest``) so no market data provider or LLM is ever contacted. Validation,
lookup and streaming behaviour is exercised against the real application.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.analysis.conftest import StubTaskQueue
from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api


class TestTriggerAnalysis(BaseAPITest):
    """``POST /api/v1/analysis/analyze``."""

    ENDPOINT = "/api/v1/analysis/analyze"
    METHOD = "post"

    def test_queues_a_single_stock_in_async_mode(
        self, api_client: TestClient, stub_task_queue: StubTaskQueue
    ) -> None:
        """A single async submission returns ``202`` with the new task id."""
        response = api_client.post(self.ENDPOINT, json={"stock_code": "600519", "async_mode": True})

        assert response.status_code == 202, response.text
        body = response.json()
        assert body["status"] == "pending"
        assert body["task_id"] == "stub-task-0"
        assert stub_task_queue.batch_submissions[0]["stock_codes"] == ["600519"]

    def test_queues_a_batch_in_async_mode(
        self, api_client: TestClient, stub_task_queue: StubTaskQueue
    ) -> None:
        """A batch submission summarises accepted and skipped codes."""
        response = api_client.post(
            self.ENDPOINT,
            json={"stock_codes": ["600519", "000858"], "async_mode": True},
        )

        assert response.status_code == 202, response.text
        body = response.json()
        assert [item["stock_code"] for item in body["accepted"]] == ["600519", "000858"]
        assert body["duplicates"] == []

    def test_deduplicates_equivalent_stock_codes(
        self, api_client: TestClient, stub_task_queue: StubTaskQueue
    ) -> None:
        """Suffixed and bare forms of one code are merged into a single task."""
        api_client.post(
            self.ENDPOINT,
            json={"stock_codes": ["600519", "600519.SH"], "async_mode": True},
        )

        assert stub_task_queue.batch_submissions[0]["stock_codes"] == ["600519"]

    def test_rejects_a_request_without_any_stock_code(self, api_client: TestClient) -> None:
        """Either ``stock_code`` or ``stock_codes`` must be supplied."""
        response = api_client.post(self.ENDPOINT, json={"async_mode": True})

        self.assert_error(response, 400, "validation_error")

    def test_rejects_obviously_invalid_free_text(self, api_client: TestClient) -> None:
        """Mixed alphanumeric noise is refused before any resolver work."""
        response = api_client.post(
            self.ENDPOINT, json={"stock_code": "abc123xyz!!", "async_mode": True}
        )

        self.assert_error(response, 400, "validation_error")

    def test_rejects_an_unresolvable_stock_name(self, api_client: TestClient) -> None:
        """Free-text input must resolve to a known stock."""
        response = api_client.post(
            self.ENDPOINT, json={"stock_code": "不存在的公司名称", "async_mode": True}
        )

        self.assert_error(response, 400, "validation_error")

    def test_rejects_a_batch_above_the_size_limit(self, api_client: TestClient) -> None:
        """A single request may not exceed fifty stocks."""
        codes = [f"6{index:05d}" for index in range(51)]

        response = api_client.post(self.ENDPOINT, json={"stock_codes": codes, "async_mode": True})

        self.assert_error(response, 400, "validation_error")

    def test_rejects_multiple_stocks_in_synchronous_mode(self, api_client: TestClient) -> None:
        """Synchronous analysis only supports one stock per request."""
        response = api_client.post(
            self.ENDPOINT, json={"stock_codes": ["600519", "000858"], "async_mode": False}
        )

        self.assert_error(response, 400, "validation_error")

    def test_rejects_an_unknown_report_type(self, api_client: TestClient) -> None:
        """``report_type`` is restricted to the documented values."""
        response = api_client.post(
            self.ENDPOINT,
            json={"stock_code": "600519", "report_type": "novel", "async_mode": True},
        )

        self.assert_validation_error(response, field="report_type")

    def test_reports_a_duplicate_submission(
        self, api_client: TestClient, stub_task_queue: StubTaskQueue
    ) -> None:
        """A stock already under analysis is rejected with ``409``."""

        class _Duplicate(Exception):
            stock_code = "600519"
            existing_task_id = "existing-task"

            def __str__(self) -> str:
                return "600519 正在分析中"

        stub_task_queue.duplicates.append(_Duplicate())

        response = api_client.post(self.ENDPOINT, json={"stock_code": "600519", "async_mode": True})

        body = self.assert_error(response, 409, "duplicate_task")
        assert body["stock_code"] == "600519"
        assert body["existing_task_id"] == "existing-task"

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Analysis submission is only available to an authenticated admin."""
        response = auth_enabled_client.post(self.ENDPOINT, json={"stock_code": "600519"})

        self.assert_unauthorized(response)


class TestTriggerMarketReview(BaseAPITest):
    """``POST /api/v1/analysis/market-review``."""

    ENDPOINT = "/api/v1/analysis/market-review"
    METHOD = "post"

    def test_accepts_a_review_request(
        self, api_client: TestClient, api_spec: dict[str, Any], stub_task_queue: StubTaskQueue
    ) -> None:
        """A review is queued in the background and acknowledged with ``202``."""
        response = api_client.post(self.ENDPOINT, json={"send_notification": False})

        body = self.assert_matches_spec(api_spec, response)
        assert body["status"] == "accepted"
        assert body["send_notification"] is False
        assert body["task_id"]
        assert stub_task_queue.background_submissions[0]["stock_code"] == "market_review"

    def test_accepts_an_empty_body(
        self, api_client: TestClient, stub_task_queue: StubTaskQueue
    ) -> None:
        """All review options are optional."""
        response = api_client.post(self.ENDPOINT)

        assert response.status_code == 202, response.text

    def test_rejects_a_concurrent_review(
        self, api_client: TestClient, stub_task_queue: StubTaskQueue
    ) -> None:
        """Only one review may run at a time on a single host."""
        assert api_client.post(self.ENDPOINT).status_code == 202

        response = api_client.post(self.ENDPOINT)

        self.assert_error(response, 409, "duplicate_market_review")

    def test_rejects_a_non_boolean_notification_flag(self, api_client: TestClient) -> None:
        """``send_notification`` must be a boolean."""
        response = api_client.post(self.ENDPOINT, json={"send_notification": "maybe"})

        self.assert_validation_error(response, field="send_notification")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Market review submission requires an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.post(self.ENDPOINT))


class TestGetTaskList(BaseAPITest):
    """``GET /api/v1/analysis/tasks``."""

    ENDPOINT = "/api/v1/analysis/tasks"
    METHOD = "get"

    def test_returns_an_empty_queue_summary(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A fresh process has no queued or running analysis tasks."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body["tasks"] == []
        assert body["pending"] == 0
        assert body["processing"] == 0

    def test_accepts_a_comma_separated_status_filter(self, api_client: TestClient) -> None:
        """Multiple statuses may be requested in one call."""
        body = self.assert_ok(
            api_client.get(self.ENDPOINT, params={"status": "pending,processing"})
        )

        assert body["tasks"] == []

    def test_rejects_a_limit_above_the_maximum(self, api_client: TestClient) -> None:
        """``limit`` is capped at one hundred."""
        response = api_client.get(self.ENDPOINT, params={"limit": 101})

        self.assert_validation_error(response, field="limit")

    def test_rejects_a_limit_below_the_minimum(self, api_client: TestClient) -> None:
        """``limit`` must be at least one."""
        response = api_client.get(self.ENDPOINT, params={"limit": 0})

        self.assert_validation_error(response, field="limit")

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """The task list is only readable by an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.get(self.ENDPOINT))


class TestTaskStream(BaseAPITest):
    """``GET /api/v1/analysis/tasks/stream``."""

    ENDPOINT = "/api/v1/analysis/tasks/stream"
    METHOD = "get"

    def test_opens_a_server_sent_event_stream(self, api_client: TestClient) -> None:
        """The stream announces itself with a ``connected`` event.

        The endpoint never completes, and the in-process ASGI transport buffers
        whole responses, so the streaming response is consumed directly instead
        of through the HTTP client.
        """
        from api.v1.endpoints.analysis import task_stream

        async def read_first_event() -> tuple[str, str]:
            response = await task_stream()
            events = response.body_iterator
            try:
                first_chunk = await anext(events)
            finally:
                await events.aclose()
            return response.media_type, first_chunk

        media_type, first_chunk = asyncio.run(read_first_event())

        assert media_type == "text/event-stream"
        assert first_chunk.startswith("event: connected")

    def test_is_documented_as_an_event_stream(self, api_spec: dict[str, Any]) -> None:
        """The contract advertises the ``text/event-stream`` content type."""
        operation = self.operation(api_spec)

        assert "text/event-stream" in operation["responses"]["200"]["content"]

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """The event stream is only available to an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.get(self.ENDPOINT))


class TestGetAnalysisStatus(BaseAPITest):
    """``GET /api/v1/analysis/status/{task_id}``."""

    ENDPOINT = "/api/v1/analysis/status/{task_id}"
    METHOD = "get"

    def test_reports_an_unknown_task_as_missing(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Expired or unknown task ids return ``404``."""
        response = api_client.get("/api/v1/analysis/status/missing-task")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Task status is only readable by an authenticated admin."""
        self.assert_unauthorized(auth_enabled_client.get("/api/v1/analysis/status/missing-task"))


class TestGetTaskRunFlow(BaseAPITest):
    """``GET /api/v1/analysis/tasks/{task_id}/flow``."""

    ENDPOINT = "/api/v1/analysis/tasks/{task_id}/flow"
    METHOD = "get"

    def test_reports_an_unknown_task_as_missing(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """A run flow is only available for a known task."""
        response = api_client.get("/api/v1/analysis/tasks/missing-task/flow")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)

    def test_requires_authentication_when_enabled(self, auth_enabled_client: TestClient) -> None:
        """Run flows are only readable by an authenticated admin."""
        self.assert_unauthorized(
            auth_enabled_client.get("/api/v1/analysis/tasks/missing-task/flow")
        )
