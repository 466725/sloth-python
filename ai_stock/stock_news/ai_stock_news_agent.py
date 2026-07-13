from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from .provider import CompositeNewsProvider


NewsProvider = Callable[..., Any]


@dataclass
class StockNewsContext:
    symbol: str
    market: str
    news_items: List[Dict[str, Any]]
    sentiment_score: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "market": self.market,
            "news_items": self.news_items,
            "sentiment_score": self.sentiment_score,
        }


class AIStockNewsAgent:
    """Collects and scores company-related news for prediction use."""

    POSITIVE_KEYWORDS = {
        "beat",
        "upgrade",
        "growth",
        "profit",
        "record",
        "contract",
        "approval",
    }
    NEGATIVE_KEYWORDS = {
        "miss",
        "downgrade",
        "lawsuit",
        "fraud",
        "loss",
        "investigation",
        "default",
    }

    def __init__(self, news_provider: Optional[NewsProvider] = None) -> None:
        self.news_provider = news_provider or CompositeNewsProvider()

    def collect_context(
        self,
        symbol: str,
        market: str = "cn",
        limit: int = 20,
    ) -> StockNewsContext:
        raw_news = self._safe_call(self.news_provider, symbol=symbol, market=market, limit=limit)
        news_items = self._normalize_news(raw_news)
        sentiment_score = self._estimate_sentiment(news_items)

        return StockNewsContext(
            symbol=symbol,
            market=market,
            news_items=news_items,
            sentiment_score=sentiment_score,
        )

    @staticmethod
    def _safe_call(provider: Optional[NewsProvider], **kwargs: Any) -> Any:
        if provider is None:
            return []
        return provider(**kwargs)

    @staticmethod
    def _normalize_news(payload: Any) -> List[Dict[str, Any]]:
        if payload is None:
            return []
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        if isinstance(payload, dict):
            return [payload]
        return []

    def _estimate_sentiment(self, news_items: List[Dict[str, Any]]) -> int:
        score = 0
        for item in news_items:
            text = " ".join(str(item.get(k, "")) for k in ("title", "summary", "content")).lower()
            score += sum(1 for kw in self.POSITIVE_KEYWORDS if kw in text)
            score -= sum(1 for kw in self.NEGATIVE_KEYWORDS if kw in text)
        return score
