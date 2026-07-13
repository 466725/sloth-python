from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import requests

from .base import NewsFetcher, normalize_text

logger = logging.getLogger(__name__)

_AV_BASE_URL = "https://www.alphavantage.co/query"


def _to_av_time(value: datetime) -> str:
    return value.strftime("%Y%m%dT%H%M")


class AlphaVantageNewsFetcher(NewsFetcher):
    """Fetch company news from Alpha Vantage NEWS_SENTIMENT."""

    source = "alphavantage"

    def __init__(self) -> None:
        self._api_key = os.getenv("ALPHAVANTAGE_API_KEY")

    def fetch_company_news(self, symbol: str, market: str = "cn", limit: int = 20) -> List[Dict[str, Any]]:
        if not self._api_key:
            return []

        ticker = normalize_text(symbol).upper()
        if not ticker:
            return []

        now = datetime.now(timezone.utc)
        start = now - timedelta(days=14)

        try:
            response = requests.get(
                _AV_BASE_URL,
                params={
                    "function": "NEWS_SENTIMENT",
                    "tickers": ticker,
                    "time_from": _to_av_time(start),
                    "time_to": _to_av_time(now),
                    "limit": max(limit, 20),
                    "apikey": self._api_key,
                },
                timeout=20,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            logger.debug("AlphaVantage news fetch failed for %s: %s", ticker, exc)
            return []

        feed = payload.get("feed") if isinstance(payload, dict) else None
        if not isinstance(feed, list):
            return []

        news_items: List[Dict[str, Any]] = []
        for raw in feed[: max(limit * 3, limit)]:
            if not isinstance(raw, dict):
                continue
            title = normalize_text(raw.get("title"))
            if not title:
                continue
            news_items.append(
                {
                    "source": self.source,
                    "symbol": ticker,
                    "title": title,
                    "summary": normalize_text(raw.get("summary")),
                    "content": normalize_text(raw.get("summary")),
                    "url": normalize_text(raw.get("url")),
                    "published_at": normalize_text(raw.get("time_published")),
                    "raw": raw,
                }
            )
        return news_items[:limit]
