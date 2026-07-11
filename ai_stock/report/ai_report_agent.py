from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class PredictionOutcome:
    direction: str
    confidence: float
    reason: str


class AIReportAgent:
    """Builds final prediction reports from coordinator outputs."""

    def build_report(
        self,
        symbol: str,
        market: str,
        prediction: PredictionOutcome,
        strategy_names: List[str],
        stock_data: Dict[str, Any],
        stock_news: Dict[str, Any],
    ) -> Dict[str, Any]:
        generated_at = datetime.now(timezone.utc).isoformat()
        report_text = self._render_markdown(
            symbol=symbol,
            market=market,
            generated_at=generated_at,
            prediction=prediction,
            strategy_names=strategy_names,
            stock_data=stock_data,
            stock_news=stock_news,
        )

        return {
            "generated_at": generated_at,
            "symbol": symbol,
            "market": market,
            "prediction": {
                "direction": prediction.direction,
                "confidence": prediction.confidence,
                "reason": prediction.reason,
            },
            "strategy_names": strategy_names,
            "stock_data": stock_data,
            "stock_news": stock_news,
            "report_markdown": report_text,
        }

    @staticmethod
    def _render_markdown(
        symbol: str,
        market: str,
        generated_at: str,
        prediction: PredictionOutcome,
        strategy_names: List[str],
        stock_data: Dict[str, Any],
        stock_news: Dict[str, Any],
    ) -> str:
        history_count = len(stock_data.get("history", []))
        news_count = len(stock_news.get("news_items", []))

        return "\n".join(
            [
                f"# AI Stock Prediction Report - {symbol}",
                "",
                f"- Generated At (UTC): {generated_at}",
                f"- Market: {market}",
                f"- Direction: {prediction.direction}",
                f"- Confidence: {prediction.confidence:.2f}",
                f"- Reason: {prediction.reason}",
                "",
                "## Applied Strategies",
                f"- {', '.join(strategy_names) if strategy_names else 'none'}",
                "",
                "## Data Summary",
                f"- History rows: {history_count}",
                f"- News items: {news_count}",
                f"- News sentiment score: {stock_news.get('sentiment_score', 0)}",
            ]
        )
