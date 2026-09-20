from __future__ import annotations

import os
from typing import Any, Dict, Optional

import pytest

from ai_stock.stock_news import finnhub_news_fetcher as module


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
    monkeypatch.delenv("FINNHUB_API_KEY", raising=False)

    def _should_not_call(*args: Any, **kwargs: Any) -> Any:  # pragma: no cover - safety guard
        raise AssertionError("requests.get should not be called when API key is missing")

    monkeypatch.setattr(module.requests, "get", _should_not_call)

    fetcher = module.FinnhubNewsFetcher()
    assert fetcher.fetch_company_news("AAPL", market="us", limit=5) == []


@pytest.mark.unit
def test_fetch_company_news_parses_useful_items(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")

    captured_params: Dict[str, Any] = {}

    payload = [
        {
            "headline": "Apple signs major contract",
            "summary": "New enterprise deal may boost growth.",
            "url": "https://example.test/apple-contract",
            "datetime": 1783928400,
        },
        {
            "headline": "",
            "summary": "Should be filtered because headline is empty",
            "url": "https://example.test/invalid",
            "datetime": 1783920000,
        },
        "invalid-item",
    ]

    def _fake_get(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 0) -> _DummyResponse:
        captured_params.update(params or {})
        assert url == f"{module._FINNHUB_BASE_URL}/company-news"
        assert timeout == 15
        return _DummyResponse(payload)

    monkeypatch.setattr(module.requests, "get", _fake_get)

    fetcher = module.FinnhubNewsFetcher()
    items = fetcher.fetch_company_news("aapl", market="us", limit=3)

    assert len(items) == 1
    item = items[0]
    assert item["source"] == "finnhub"
    assert item["symbol"] == "AAPL"
    assert item["title"] == "Apple signs major contract"
    assert item["summary"] == "New enterprise deal may boost growth."
    assert item["content"] == "New enterprise deal may boost growth."
    assert item["url"] == "https://example.test/apple-contract"
    assert isinstance(item["published_at"], str)
    assert item["published_at"]

    assert captured_params["symbol"] == "AAPL"
    assert captured_params["token"] == "test-key"
    assert captured_params["from"] == "2020-01-01"
    assert captured_params["to"] == "2030-01-01"


@pytest.mark.unit
def test_fetch_company_news_handles_request_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")

    def _fake_get(*args: Any, **kwargs: Any) -> _DummyResponse:
        raise RuntimeError("network down")

    monkeypatch.setattr(module.requests, "get", _fake_get)

    fetcher = module.FinnhubNewsFetcher()
    assert fetcher.fetch_company_news("AAPL", market="us", limit=10) == []


@pytest.mark.unit
def test_fetch_company_news_returns_empty_when_payload_not_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")

    def _fake_get(*args: Any, **kwargs: Any) -> _DummyResponse:
        return _DummyResponse({"note": "unexpected payload"})

    monkeypatch.setattr(module.requests, "get", _fake_get)

    fetcher = module.FinnhubNewsFetcher()
    assert fetcher.fetch_company_news("AAPL", market="us", limit=10) == []


@pytest.mark.api
def test_fetch_company_news_live_returns_useful_news() -> None:
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        pytest.skip("FINNHUB_API_KEY is not configured")

    fetcher = module.FinnhubNewsFetcher()
    items = fetcher.fetch_company_news("AAPL", market="us", limit=10)

    assert items, "Expected live Finnhub news, got empty list"

    useful_count = 0
    for item in items:
        title = str(item.get("title", "")).strip()
        summary = str(item.get("summary", "")).strip()
        url = str(item.get("url", "")).strip()
        if title and (summary or url):
            useful_count += 1

    assert useful_count > 0, f"Expected at least one useful news item, got: {items}"
