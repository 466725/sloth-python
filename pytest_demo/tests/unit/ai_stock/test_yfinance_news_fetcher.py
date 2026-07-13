from __future__ import annotations

import os
import sys
from types import SimpleNamespace
from typing import Any, Dict

import pytest

from ai_stock.stock_news import yfinance_news_fetcher as module


@pytest.mark.unit
def test_fetch_company_news_returns_empty_when_symbol_blank() -> None:
    fetcher = module.YFinanceNewsFetcher()
    assert fetcher.fetch_company_news("", market="us", limit=5) == []
    assert fetcher.fetch_company_news("   ", market="us", limit=5) == []


@pytest.mark.unit
def test_fetch_company_news_parses_useful_items(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: Dict[str, Any] = {}

    payload = [
        {
            "title": "Apple launches new AI features",
            "summary": "New on-device model announced.",
            "link": "https://example.test/apple-ai",
            "providerPublishTime": 1783928400,
        },
        {
            "title": "Apple expands data centers",
            "summary": "",
            "content": {"summary": "Capacity increase supports growth."},
            "url": "https://example.test/apple-dc",
            "providerPublishTime": 1783928500,
        },
        {
            "title": "",
            "summary": "Should be filtered because title is empty",
            "link": "https://example.test/invalid",
            "providerPublishTime": 1783928600,
        },
        "invalid-item",
    ]

    class _FakeTicker:
        def __init__(self, symbol: str) -> None:
            captured["symbol"] = symbol
            self.news = payload

    fake_yf = SimpleNamespace(Ticker=_FakeTicker)
    monkeypatch.setitem(sys.modules, "yfinance", fake_yf)

    fetcher = module.YFinanceNewsFetcher()
    items = fetcher.fetch_company_news("aapl", market="us", limit=5)

    assert captured["symbol"] == "AAPL"
    assert len(items) == 2

    first = items[0]
    assert first["source"] == "yfinance"
    assert first["symbol"] == "AAPL"
    assert first["title"] == "Apple launches new AI features"
    assert first["summary"] == "New on-device model announced."
    assert first["content"] == "New on-device model announced."
    assert first["url"] == "https://example.test/apple-ai"
    assert first["published_at"] == 1783928400

    second = items[1]
    assert second["title"] == "Apple expands data centers"
    assert second["summary"] == ""
    assert second["content"] == "Capacity increase supports growth."
    assert second["url"] == "https://example.test/apple-dc"


@pytest.mark.unit
def test_fetch_company_news_handles_ticker_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    class _BrokenYf:
        @staticmethod
        def Ticker(symbol: str) -> Any:
            raise RuntimeError(f"failed for {symbol}")

    monkeypatch.setitem(sys.modules, "yfinance", _BrokenYf)

    fetcher = module.YFinanceNewsFetcher()
    assert fetcher.fetch_company_news("AAPL", market="us", limit=10) == []


@pytest.mark.unit
def test_fetch_company_news_returns_empty_when_payload_not_list(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FakeTicker:
        def __init__(self, symbol: str) -> None:
            self.news = {"unexpected": "shape"}

    fake_yf = SimpleNamespace(Ticker=_FakeTicker)
    monkeypatch.setitem(sys.modules, "yfinance", fake_yf)

    fetcher = module.YFinanceNewsFetcher()
    assert fetcher.fetch_company_news("AAPL", market="us", limit=10) == []


@pytest.mark.api
def test_fetch_company_news_live_returns_useful_news() -> None:
    if os.getenv("RUN_LIVE_YFINANCE_TESTS") != "1":
        pytest.skip("Set RUN_LIVE_YFINANCE_TESTS=1 to run live yfinance news check")

    fetcher = module.YFinanceNewsFetcher()
    items = fetcher.fetch_company_news("AAPL", market="us", limit=10)

    assert items, "Expected live yfinance news, got empty list"

    useful_count = 0
    for item in items:
        title = str(item.get("title", "")).strip()
        summary = str(item.get("summary", "")).strip()
        url = str(item.get("url", "")).strip()
        if title and (summary or url):
            useful_count += 1

    assert useful_count > 0, f"Expected at least one useful news item, got: {items}"
