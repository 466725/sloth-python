from __future__ import annotations

import os
import sys
from types import SimpleNamespace
from typing import Any

import pytest

from ai_stock.stock_news import yfinance_news_fetcher as module

NEWS_PAYLOAD = [
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


def _install_yfinance(monkeypatch: pytest.MonkeyPatch, ticker_factory: Any) -> None:
    monkeypatch.setitem(sys.modules, "yfinance", SimpleNamespace(Ticker=ticker_factory))


def _assert_useful_news(items: list[dict[str, Any]]) -> None:
    assert items, "Expected useful yfinance news, got empty list"
    assert any(
        str(item.get("title", "")).strip()
        and (
            str(item.get("summary", "")).strip()
            or str(item.get("url", "")).strip()
        )
        for item in items
    ), f"Expected at least one useful news item, got: {items}"


@pytest.mark.unit
@pytest.mark.parametrize("symbol", ["", "   "])
def test_fetch_company_news_returns_empty_when_symbol_blank(symbol: str) -> None:
    fetcher = module.YFinanceNewsFetcher()
    assert fetcher.fetch_company_news(symbol, market="us", limit=5) == []


@pytest.mark.unit
def test_fetch_company_news_parses_useful_items(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, str] = {}

    class _FakeTicker:
        def __init__(self, symbol: str) -> None:
            captured["symbol"] = symbol
            self.news = NEWS_PAYLOAD

    _install_yfinance(monkeypatch, _FakeTicker)

    fetcher = module.YFinanceNewsFetcher()
    items = fetcher.fetch_company_news("aapl", market="us", limit=5)

    assert captured["symbol"] == "AAPL"
    assert items == [
        {
            "source": "yfinance",
            "symbol": "AAPL",
            "title": "Apple launches new AI features",
            "summary": "New on-device model announced.",
            "content": "New on-device model announced.",
            "url": "https://example.test/apple-ai",
            "published_at": 1783928400,
            "raw": NEWS_PAYLOAD[0],
        },
        {
            "source": "yfinance",
            "symbol": "AAPL",
            "title": "Apple expands data centers",
            "summary": "",
            "content": "Capacity increase supports growth.",
            "url": "https://example.test/apple-dc",
            "published_at": 1783928500,
            "raw": NEWS_PAYLOAD[1],
        },
    ]


@pytest.mark.unit
def test_fetch_company_news_handles_ticker_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def _broken_ticker(symbol: str) -> Any:
        raise RuntimeError(f"failed for {symbol}")

    _install_yfinance(monkeypatch, _broken_ticker)

    fetcher = module.YFinanceNewsFetcher()
    assert fetcher.fetch_company_news("AAPL", market="us", limit=10) == []


@pytest.mark.unit
def test_fetch_company_news_returns_empty_when_payload_not_list(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FakeTicker:
        def __init__(self, symbol: str) -> None:
            self.news = {"unexpected": "shape"}

    _install_yfinance(monkeypatch, _FakeTicker)

    fetcher = module.YFinanceNewsFetcher()
    assert fetcher.fetch_company_news("AAPL", market="us", limit=10) == []


@pytest.mark.api
def test_fetch_company_news_live_returns_useful_news() -> None:
    if os.getenv("RUN_LIVE_YFINANCE_TESTS") != "1":
        pytest.skip("Set RUN_LIVE_YFINANCE_TESTS=1 to run live yfinance news check")

    fetcher = module.YFinanceNewsFetcher()
    items = fetcher.fetch_company_news("AAPL", market="us", limit=10)

    assert items, "Expected live yfinance news, got empty list"

    _assert_useful_news(items)
