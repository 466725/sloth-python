from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


Provider = Callable[..., Any]


@dataclass
class StockDataContext:
    symbol: str
    market: str
    history: List[Dict[str, Any]]
    realtime_quote: Dict[str, Any]
    fundamentals: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "market": self.market,
            "history": self.history,
            "realtime_quote": self.realtime_quote,
            "fundamentals": self.fundamentals,
        }


class AIStockDataAgent:
    """Collects stock market data needed by prediction strategies.

    The agent is provider-driven so callers can wire any data backend
    (existing fetchers, manager classes, API wrappers, etc.).
    """

    def __init__(
        self,
        history_provider: Optional[Provider] = None,
        realtime_provider: Optional[Provider] = None,
        fundamentals_provider: Optional[Provider] = None,
    ) -> None:
        self.history_provider = history_provider
        self.realtime_provider = realtime_provider
        self.fundamentals_provider = fundamentals_provider

    def collect_context(
        self,
        symbol: str,
        market: str = "cn",
        lookback_days: int = 120,
    ) -> StockDataContext:
        history = self._safe_call(self.history_provider, symbol=symbol, market=market, lookback_days=lookback_days)
        realtime_quote = self._safe_call(self.realtime_provider, symbol=symbol, market=market)
        fundamentals = self._safe_call(self.fundamentals_provider, symbol=symbol, market=market)

        return StockDataContext(
            symbol=symbol,
            market=market,
            history=self._normalize_list_of_dict(history),
            realtime_quote=self._normalize_dict(realtime_quote),
            fundamentals=self._normalize_dict(fundamentals),
        )

    @staticmethod
    def _safe_call(provider: Optional[Provider], **kwargs: Any) -> Any:
        if provider is None:
            return {}
        return provider(**kwargs)

    @staticmethod
    def _normalize_list_of_dict(payload: Any) -> List[Dict[str, Any]]:
        if payload is None:
            return []
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        if isinstance(payload, dict):
            return [payload]
        return []

    @staticmethod
    def _normalize_dict(payload: Any) -> Dict[str, Any]:
        if payload is None:
            return {}
        if isinstance(payload, dict):
            return payload
        return {"value": payload}
