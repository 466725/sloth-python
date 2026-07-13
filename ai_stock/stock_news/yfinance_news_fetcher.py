from __future__ import annotations

import logging
from typing import Any, Dict, List

from .base import NewsFetcher, normalize_text

logger = logging.getLogger(__name__)


class YFinanceNewsFetcher(NewsFetcher):
    """Fetch company news from yfinance ticker.news payload."""

    source = "yfinance"

    def fetch_company_news(self, symbol: str, market: str = "cn", limit: int = 20) -> List[Dict[str, Any]]:
        ticker_symbol = normalize_text(symbol).upper()
        if not ticker_symbol:
            return []

        try:
            import yfinance as yf

            ticker = yf.Ticker(ticker_symbol)
            payload = getattr(ticker, "news", [])
        except Exception as exc:  # pragma: no cover - optional dependency/network path
            logger.debug("YFinance news fetch failed for %s: %s", ticker_symbol, exc)
            return []

        if not isinstance(payload, list):
            return []

        news_items: List[Dict[str, Any]] = []
        for raw in payload[: max(limit * 3, limit)]:
            if not isinstance(raw, dict):
                continue
            title = normalize_text(raw.get("title"))
            if not title:
                continue
            summary = normalize_text(raw.get("summary"))
            content = summary
            if not content:
                content_blocks = raw.get("content")
                if isinstance(content_blocks, dict):
                    content = normalize_text(content_blocks.get("summary"))
            news_items.append(
                {
                    "source": self.source,
                    "symbol": ticker_symbol,
                    "title": title,
                    "summary": summary,
                    "content": content,
                    "url": normalize_text(raw.get("link")) or normalize_text(raw.get("url")),
                    "published_at": raw.get("providerPublishTime"),
                    "raw": raw,
                }
            )
        return news_items[:limit]
