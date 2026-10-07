"""API tests for the stock market-data endpoints.

``StockService`` is patched in every test: these endpoints would otherwise call
live market-data providers, which is neither deterministic nor offline-safe.
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api

QUOTE = {
    "stock_code": "600519",
    "stock_name": "贵州茅台",
    "current_price": 1688.0,
    "change": 12.5,
    "change_percent": 0.75,
    "open": 1670.0,
    "high": 1695.0,
    "low": 1665.0,
    "prev_close": 1675.5,
    "volume": 32100,
    "amount": 5.4e9,
    "update_time": "2026-01-05 15:00:00",
}

HISTORY = {
    "stock_name": "贵州茅台",
    "data": [
        {
            "date": "2026-01-05",
            "open": 1670.0,
            "high": 1695.0,
            "low": 1665.0,
            "close": 1688.0,
            "volume": 32100,
            "amount": 5.4e9,
            "change_percent": 0.75,
        }
    ],
}


@pytest.fixture
def stub_stock_service(monkeypatch: pytest.MonkeyPatch) -> None:
    """Replace the market-data provider with deterministic offline responses."""
    import api.v1.endpoints.stocks as stocks_endpoint

    class _StubStockService:
        def get_realtime_quote(self, stock_code: str) -> dict[str, Any] | None:
            return None if stock_code == "999999" else dict(QUOTE, stock_code=stock_code)

        def get_history_data(self, stock_code: str, period: str, days: int) -> dict[str, Any]:
            if period != "daily":
                raise ValueError(f"unsupported period: {period}")
            return HISTORY

    monkeypatch.setattr(stocks_endpoint, "StockService", _StubStockService)


class TestStockQuote(BaseAPITest):
    """``GET /api/v1/stocks/{stock_code}/quote``."""

    ENDPOINT = "/api/v1/stocks/{stock_code}/quote"
    METHOD = "get"

    def test_returns_quote(
        self, api_client: TestClient, api_spec: dict[str, Any], stub_stock_service: None
    ) -> None:
        """A known stock returns its latest quote."""
        response = api_client.get("/api/v1/stocks/600519/quote")

        body = self.assert_matches_spec(api_spec, response)
        assert body["stock_code"] == "600519"
        assert body["stock_name"] == "贵州茅台"
        assert body["current_price"] == 1688.0

    def test_returns_404_when_no_quote_is_available(
        self, api_client: TestClient, api_spec: dict[str, Any], stub_stock_service: None
    ) -> None:
        """A stock without quote data reports a documented ``404``."""
        response = api_client.get("/api/v1/stocks/999999/quote")

        self.assert_not_found(response)
        self.assert_documented_status(api_spec, response)

    def test_provider_failure_reports_500(
        self, api_client: TestClient, api_spec: dict[str, Any], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A provider outage surfaces as a documented ``500``."""
        import api.v1.endpoints.stocks as stocks_endpoint

        class _FailingStockService:
            def get_realtime_quote(self, stock_code: str) -> dict[str, Any]:
                raise RuntimeError("provider unavailable")

        monkeypatch.setattr(stocks_endpoint, "StockService", _FailingStockService)

        response = api_client.get("/api/v1/stocks/600519/quote")

        self.assert_error(response, 500, "internal_error")
        self.assert_documented_status(api_spec, response)


class TestStockHistory(BaseAPITest):
    """``GET /api/v1/stocks/{stock_code}/history``."""

    ENDPOINT = "/api/v1/stocks/{stock_code}/history"
    METHOD = "get"

    def test_returns_daily_candles(
        self, api_client: TestClient, api_spec: dict[str, Any], stub_stock_service: None
    ) -> None:
        """The default request returns daily K-line data."""
        response = api_client.get("/api/v1/stocks/600519/history")

        body = self.assert_matches_spec(api_spec, response)
        assert body["stock_code"] == "600519"
        assert body["period"] == "daily"
        assert body["data"][0]["close"] == 1688.0

    def test_unsupported_period_reports_422(
        self, api_client: TestClient, api_spec: dict[str, Any], stub_stock_service: None
    ) -> None:
        """A period the provider cannot serve reports a documented ``422``."""
        response = api_client.get("/api/v1/stocks/600519/history", params={"period": "weekly"})

        self.assert_error(response, 422, "unsupported_period")
        self.assert_documented_status(api_spec, response)

    def test_rejects_period_outside_the_pattern(self, api_client: TestClient) -> None:
        """``period`` must match the documented ``daily|weekly|monthly`` pattern."""
        response = api_client.get("/api/v1/stocks/600519/history", params={"period": "hourly"})

        self.assert_validation_error(response, field="period")

    @pytest.mark.parametrize("days", [0, -1, 366])
    def test_rejects_out_of_range_days(self, api_client: TestClient, days: int) -> None:
        """``days`` honors the documented 1..365 range."""
        response = api_client.get("/api/v1/stocks/600519/history", params={"days": days})

        self.assert_validation_error(response, field="days")
