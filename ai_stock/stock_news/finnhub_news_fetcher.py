from __future__ import annotations

import logging
import os
from typing import Any, Dict, List

import requests

from .base import NewsFetcher, normalize_text, utc_iso_from_epoch

logger = logging.getLogger(__name__)

_FINNHUB_BASE_URL = "https://finnhub.io/api/v1"


class FinnhubNewsFetcher(NewsFetcher):
    """Fetch company news from Finnhub endpoint."""

    source = "finnhub"

    def __init__(self) -> None:
        self._api_key = os.getenv("FINNHUB_API_KEY")

    def fetch_company_news(self, symbol: str, market: str = "cn", limit: int = 20) -> List[Dict[str, Any]]:
        if not self._api_key:
            return []

        ticker = normalize_text(symbol).upper()
        if not ticker:
            return []

        try:
            response = requests.get(
                f"{_FINNHUB_BASE_URL}/company-news",
                params={
                    "symbol": ticker,
                    "from": "2020-01-01",
                    "to": "2030-01-01",
                    "token": self._api_key,
                },
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:  # pragma: no cover - network failure path
            logger.debug("Finnhub news fetch failed for %s: %s", ticker, exc)
            return []

        if not isinstance(payload, list):
            return []

        news_items: List[Dict[str, Any]] = []
        for raw in payload[: max(limit * 3, limit)]:
            if not isinstance(raw, dict):
                continue
            title = normalize_text(raw.get("headline"))
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
                    "published_at": utc_iso_from_epoch(raw.get("datetime")),
                    "raw": raw,
                }
            )
        return news_items[:limit]
