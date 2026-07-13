from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from .alphavantage_news_fetcher import AlphaVantageNewsFetcher
from .base import NewsFetcher, deduplicate_news, limit_news, normalize_text
from .finnhub_news_fetcher import FinnhubNewsFetcher
from .yfinance_news_fetcher import YFinanceNewsFetcher


class CompositeNewsProvider:
    """Collect news from multiple fetchers with fallback and deduplication."""

    def __init__(self, fetchers: Optional[Iterable[NewsFetcher]] = None) -> None:
        self.fetchers = list(fetchers) if fetchers is not None else [
            FinnhubNewsFetcher(),
            AlphaVantageNewsFetcher(),
            YFinanceNewsFetcher(),
        ]

    def __call__(self, symbol: str, market: str = "cn", limit: int = 20) -> List[Dict[str, Any]]:
        merged: List[Dict[str, Any]] = []
        for fetcher in self.fetchers:
            items = fetcher.fetch_company_news(symbol=symbol, market=market, limit=limit)
            if items:
                merged.extend(items)

        normalized = [self._normalize_item(item, symbol=symbol, market=market) for item in merged]
        normalized = [item for item in normalized if item.get("title")]
        deduped = deduplicate_news(normalized)
        sorted_items = sorted(deduped, key=self._sort_key, reverse=True)
        return limit_news(sorted_items, limit)

    @staticmethod
    def _normalize_item(item: Dict[str, Any], symbol: str, market: str) -> Dict[str, Any]:
        normalized = dict(item)
        normalized["symbol"] = normalize_text(normalized.get("symbol")) or symbol
        normalized["market"] = normalize_text(normalized.get("market")) or market
        normalized["title"] = normalize_text(normalized.get("title"))
        normalized["summary"] = normalize_text(normalized.get("summary"))
        normalized["content"] = normalize_text(normalized.get("content"))
        normalized["url"] = normalize_text(normalized.get("url"))
        return normalized

    @staticmethod
    def _sort_key(item: Dict[str, Any]) -> Any:
        value = item.get("published_at")
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str) and value:
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
            except ValueError:
                return value
        return ""
