from __future__ import annotations

import os
from typing import Any, Dict, Optional

import pytest

from ai_stock.stock_news import alphavantage_news_fetcher as module


class _DummyResponse:
    def __init__(self, payload: Any, should_raise: bool = False) -> None:
        self._payload = payload
        self._should_raise = should_raise

    def raise_for_status(self) -> None:
        if self._should_raise:
            raise RuntimeError("http error")

    def json(self) -> Any:
        return self._payload


@pytest.mark.unit
def test_fetch_company_news_returns_empty_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ALPHAVANTAGE_API_KEY", raising=False)

    def _should_not_call(*args: Any, **kwargs: Any) -> Any:  # pragma: no cover - safety guard
        raise AssertionError("requests.get should not be called when API key is missing")

    monkeypatch.setattr(module.requests, "get", _should_not_call)

    fetcher = module.AlphaVantageNewsFetcher()
    assert fetcher.fetch_company_news("AAPL", market="us", limit=5) == []


@pytest.mark.unit
def test_fetch_company_news_parses_useful_items(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "test-key")

    captured_params: Dict[str, Any] = {}

    payload = {
        "feed": [
            {
                "title": "Apple posts record profit",
                "summary": "Revenue beat expectations in Q2.",
                "url": "https://example.test/apple-profit",
                "time_published": "20260713T1100",
            },
            {
                "title": "",
                "summary": "Should be filtered because title is empty",
                "url": "https://example.test/invalid",
                "time_published": "20260713T0900",
            },
            "invalid-item",
        ]
    }

    def _fake_get(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 0) -> _DummyResponse:
        captured_params.update(params or {})
        assert url == module._AV_BASE_URL
        assert timeout == 20
        return _DummyResponse(payload)

    monkeypatch.setattr(module.requests, "get", _fake_get)

    fetcher = module.AlphaVantageNewsFetcher()
    items = fetcher.fetch_company_news("aapl", market="us", limit=3)

    assert len(items) == 1
    item = items[0]
    assert item["source"] == "alphavantage"
    assert item["symbol"] == "AAPL"
    assert item["title"] == "Apple posts record profit"
    assert item["summary"] == "Revenue beat expectations in Q2."
    assert item["content"] == "Revenue beat expectations in Q2."
    assert item["url"] == "https://example.test/apple-profit"
    assert item["published_at"] == "20260713T1100"

    assert captured_params["function"] == "NEWS_SENTIMENT"
    assert captured_params["tickers"] == "AAPL"
    assert captured_params["apikey"] == "test-key"
    assert captured_params["limit"] == 20
    assert isinstance(captured_params["time_from"], str)
    assert isinstance(captured_params["time_to"], str)


@pytest.mark.unit
def test_fetch_company_news_handles_request_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "test-key")

    def _fake_get(*args: Any, **kwargs: Any) -> _DummyResponse:
        raise RuntimeError("network down")

    monkeypatch.setattr(module.requests, "get", _fake_get)

    fetcher = module.AlphaVantageNewsFetcher()
    assert fetcher.fetch_company_news("AAPL", market="us", limit=10) == []


@pytest.mark.unit
def test_fetch_company_news_returns_empty_when_feed_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "test-key")

    def _fake_get(*args: Any, **kwargs: Any) -> _DummyResponse:
        return _DummyResponse({"note": "ok but no feed"})

    monkeypatch.setattr(module.requests, "get", _fake_get)

    fetcher = module.AlphaVantageNewsFetcher()
    assert fetcher.fetch_company_news("AAPL", market="us", limit=10) == []


@pytest.mark.api
def test_fetch_company_news_live_returns_useful_news() -> None:
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        pytest.skip("ALPHAVANTAGE_API_KEY is not configured")

    fetcher = module.AlphaVantageNewsFetcher()
    items = fetcher.fetch_company_news("AAPL", market="us", limit=10)

    assert items, "Expected live AlphaVantage news, got empty list"

    useful_count = 0
    for item in items:
        title = str(item.get("title", "")).strip()
        summary = str(item.get("summary", "")).strip()
        url = str(item.get("url", "")).strip()
        if title and (summary or url):
            useful_count += 1

    assert useful_count > 0, f"Expected at least one useful news item, got: {items}"
