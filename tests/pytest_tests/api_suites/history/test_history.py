"""API tests for the analysis-history listing, detail and deletion endpoints."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from ai_stock.storage import AnalysisHistory
from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api


class TestHistoryList(BaseAPITest):
    """``GET /api/v1/history``."""

    ENDPOINT = "/api/v1/history"
    METHOD = "get"

    def test_returns_empty_page(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """An empty database still returns a valid pagination envelope."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert self.assert_paginated(body, page=1) == []
        assert body["limit"] == 20

    def test_lists_seeded_records_newest_first(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        seeded_history: list[AnalysisHistory],
    ) -> None:
        """Seeded records are returned with their summary fields populated."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        items = self.assert_paginated(body, page=1)
        assert body["total"] == 2
        assert [item["stock_code"] for item in items] == ["000858", "600519"]
        assert items[0]["stock_name"] == "五粮液"

    def test_filters_by_stock_code(
        self, api_client: TestClient, seeded_history: list[AnalysisHistory]
    ) -> None:
        """``stock_code`` narrows the result set to a single stock."""
        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"stock_code": "600519"}))

        assert body["total"] == 1
        assert body["items"][0]["stock_code"] == "600519"

    def test_filters_by_report_type(
        self, api_client: TestClient, seeded_history: list[AnalysisHistory]
    ) -> None:
        """``report_type`` selects only matching report kinds."""
        body = self.assert_ok(
            api_client.get(self.ENDPOINT, params={"report_type": "market_review"})
        )

        assert body["total"] == 1
        assert body["items"][0]["report_type"] == "market_review"

    def test_unmatched_filter_returns_no_items(
        self, api_client: TestClient, seeded_history: list[AnalysisHistory]
    ) -> None:
        """A filter with no matches returns an empty page, not an error."""
        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"stock_code": "999999"}))

        assert body["total"] == 0
        assert body["items"] == []

    def test_paginates_results(
        self, api_client: TestClient, seeded_history: list[AnalysisHistory]
    ) -> None:
        """``page``/``limit`` slice the result set while keeping the full total."""
        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"page": 2, "limit": 1}))

        assert body["total"] == 2
        assert body["page"] == 2
        assert len(body["items"]) == 1

    @pytest.mark.parametrize(("field", "value"), [("page", 0), ("limit", 0), ("limit", 101)])
    def test_rejects_invalid_pagination(
        self, api_client: TestClient, field: str, value: int
    ) -> None:
        """Pagination bounds documented in api_spec.json are enforced."""
        response = api_client.get(self.ENDPOINT, params={field: value})

        self.assert_validation_error(response, field=field)


class TestHistoryDetail(BaseAPITest):
    """``GET /api/v1/history/{record_id}``."""

    ENDPOINT = "/api/v1/history/{record_id}"
    METHOD = "get"

    def test_returns_detail_by_record_id(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        seeded_history: list[AnalysisHistory],
    ) -> None:
        """A numeric primary key resolves to the stored analysis."""
        record = seeded_history[0]

        response = api_client.get(f"/api/v1/history/{record.id}")

        body = self.assert_matches_spec(api_spec, response)
        assert body["meta"]["id"] == record.id
        assert body["meta"]["stock_code"] == "600519"
        assert body["meta"]["query_id"] == "query-alpha"
        assert body["summary"]["sentiment_score"] == 72
        assert float(body["strategy"]["ideal_buy"]) == 1600.0

    def test_returns_detail_by_query_id(
        self, api_client: TestClient, seeded_history: list[AnalysisHistory]
    ) -> None:
        """The same endpoint also accepts the textual ``query_id``."""
        body = self.assert_ok(api_client.get("/api/v1/history/query-beta"))

        assert body["meta"]["stock_code"] == "000858"
        assert body["meta"]["stock_name"] == "五粮液"

    def test_returns_404_for_unknown_record(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """An unknown identifier reports a documented ``404``."""
        response = api_client.get("/api/v1/history/999999")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)


class TestHistoryMarkdown(BaseAPITest):
    """``GET /api/v1/history/{record_id}/markdown``."""

    ENDPOINT = "/api/v1/history/{record_id}/markdown"
    METHOD = "get"

    def test_renders_markdown_report(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        seeded_history: list[AnalysisHistory],
    ) -> None:
        """A stored record renders into non-empty Markdown content."""
        response = api_client.get(f"/api/v1/history/{seeded_history[0].id}/markdown")

        body = self.assert_matches_spec(api_spec, response)
        assert isinstance(body["content"], str)
        assert body["content"].strip()

    def test_returns_404_for_unknown_record(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Missing records report ``404`` rather than empty Markdown."""
        response = api_client.get("/api/v1/history/999999/markdown")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)


class TestHistoryNews(BaseAPITest):
    """``GET /api/v1/history/{record_id}/news``."""

    ENDPOINT = "/api/v1/history/{record_id}/news"
    METHOD = "get"

    def test_returns_empty_list_for_record_without_news(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        seeded_history: list[AnalysisHistory],
    ) -> None:
        """Records without captured news return ``200`` with an empty list."""
        response = api_client.get(f"/api/v1/history/{seeded_history[0].id}/news")

        body = self.assert_matches_spec(api_spec, response)
        assert body == {"total": 0, "items": []}

    def test_unknown_record_returns_empty_list(self, api_client: TestClient) -> None:
        """This endpoint is documented as always returning ``200``."""
        body = self.assert_ok(api_client.get("/api/v1/history/999999/news"))

        assert body["total"] == 0

    @pytest.mark.parametrize("limit", [0, 101])
    def test_rejects_out_of_range_limit(self, api_client: TestClient, limit: int) -> None:
        """``limit`` honors the documented 1..100 range."""
        response = api_client.get("/api/v1/history/1/news", params={"limit": limit})

        self.assert_validation_error(response, field="limit")


class TestHistoryDiagnostics(BaseAPITest):
    """``GET /api/v1/history/{record_id}/diagnostics``."""

    ENDPOINT = "/api/v1/history/{record_id}/diagnostics"
    METHOD = "get"

    def test_returns_diagnostics_envelope(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        seeded_history: list[AnalysisHistory],
    ) -> None:
        """A stored record exposes a diagnostics payload keyed by its ids."""
        response = api_client.get(f"/api/v1/history/{seeded_history[0].id}/diagnostics")

        self.assert_matches_spec(api_spec, response)

    def test_returns_404_for_unknown_record(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Unknown records report a documented ``404``."""
        response = api_client.get("/api/v1/history/999999/diagnostics")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)


class TestHistoryRunFlow(BaseAPITest):
    """``GET /api/v1/history/{record_id}/flow``."""

    ENDPOINT = "/api/v1/history/{record_id}/flow"
    METHOD = "get"

    def test_returns_flow_envelope(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        seeded_history: list[AnalysisHistory],
    ) -> None:
        """A stored record exposes its execution flow payload."""
        response = api_client.get(f"/api/v1/history/{seeded_history[0].id}/flow")

        self.assert_matches_spec(api_spec, response)

    def test_returns_404_for_unknown_record(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Unknown records report a documented ``404``."""
        response = api_client.get("/api/v1/history/999999/flow")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)


class TestHistoryStockBar(BaseAPITest):
    """``GET /api/v1/history/stocks``."""

    ENDPOINT = "/api/v1/history/stocks"
    METHOD = "get"

    def test_returns_empty_bar(self, api_client: TestClient, api_spec: dict[str, Any]) -> None:
        """Without history the stock bar is empty rather than missing."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert body == {"total": 0, "items": []}

    def test_lists_distinct_stocks_excluding_market_reviews(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        seeded_history: list[AnalysisHistory],
    ) -> None:
        """Only individual-stock reports appear, each once with an analysis count."""
        response = api_client.get(self.ENDPOINT)

        body = self.assert_matches_spec(api_spec, response)
        assert {item["stock_code"] for item in body["items"]} == {"600519"}
        assert body["total"] == 1
        for item in body["items"]:
            assert item["analysis_count"] >= 1

    def test_limit_caps_returned_stocks(
        self, api_client: TestClient, seeded_history: list[AnalysisHistory]
    ) -> None:
        """``limit`` truncates the stock bar."""
        body = self.assert_ok(api_client.get(self.ENDPOINT, params={"limit": 1}))

        assert body["total"] == 1

    @pytest.mark.parametrize("limit", [0, 501])
    def test_rejects_out_of_range_limit(self, api_client: TestClient, limit: int) -> None:
        """``limit`` honors the documented 1..500 range."""
        response = api_client.get(self.ENDPOINT, params={"limit": limit})

        self.assert_validation_error(response, field="limit")


class TestDeleteHistoryRecords(BaseAPITest):
    """``DELETE /api/v1/history``."""

    ENDPOINT = "/api/v1/history"
    METHOD = "delete"

    def test_deletes_requested_records(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        seeded_history: list[AnalysisHistory],
    ) -> None:
        """Deleting by primary key removes exactly the requested records."""
        response = api_client.request(
            "DELETE", self.ENDPOINT, json={"record_ids": [seeded_history[0].id]}
        )

        body = self.assert_matches_spec(api_spec, response)
        assert body["deleted"] == 1
        assert self.assert_ok(api_client.get(self.ENDPOINT))["total"] == 1

    def test_deleting_unknown_record_reports_zero(self, api_client: TestClient) -> None:
        """Unknown ids are a no-op rather than an error."""
        body = self.assert_ok(
            api_client.request("DELETE", self.ENDPOINT, json={"record_ids": [999999]})
        )

        assert body["deleted"] == 0

    def test_rejects_empty_record_ids(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """An empty id list is rejected before touching the database."""
        response = api_client.request("DELETE", self.ENDPOINT, json={"record_ids": []})

        self.assert_error(response, 400, "invalid_request")
        self.assert_documented_status(api_spec, response)

    def test_omitted_record_ids_is_rejected_like_an_empty_list(
        self, api_client: TestClient
    ) -> None:
        """``record_ids`` defaults to an empty list and is rejected the same way."""
        response = api_client.request("DELETE", self.ENDPOINT, json={})

        self.assert_error(response, 400, "invalid_request")


class TestDeleteHistoryByCode(BaseAPITest):
    """``DELETE /api/v1/history/by-code/{stock_code}``."""

    ENDPOINT = "/api/v1/history/by-code/{stock_code}"
    METHOD = "delete"

    def test_deletes_every_record_for_the_code(
        self,
        api_client: TestClient,
        api_spec: dict[str, Any],
        seeded_history: list[AnalysisHistory],
    ) -> None:
        """All records of one stock are removed in a single call."""
        response = api_client.delete("/api/v1/history/by-code/600519")

        body = self.assert_matches_spec(api_spec, response)
        assert body["deleted"] == 1
        assert self.assert_ok(api_client.get("/api/v1/history"))["total"] == 1

    def test_unknown_code_reports_zero_deleted(self, api_client: TestClient) -> None:
        """A code without history deletes nothing and still returns ``200``."""
        body = self.assert_ok(api_client.delete("/api/v1/history/by-code/999999"))

        assert body["deleted"] == 0
