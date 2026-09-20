from __future__ import annotations

import html
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Union

# AI Stock Prediction Report Agent
@dataclass
class PredictionOutcome:
    direction: str
    confidence: float
    reason: str


# Direction -> straightforward, human-facing advice.
_ADVICE_BY_DIRECTION = {
    "up": "BUY",
    "down": "SELL",
    "sideways": "HOLD",
}

HTML_TEMPLATE_PATH = Path(__file__).with_name("html_report") / "template.html"
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# AI Report Agent
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
        advice = self._derive_advice(prediction)
        report_text = self._render_markdown(
            symbol=symbol,
            market=market,
            generated_at=generated_at,
            prediction=prediction,
            advice=advice,
            strategy_names=strategy_names,
            stock_data=stock_data,
            stock_news=stock_news,
        )
        report_html = self._render_html(
            symbol=symbol,
            market=market,
            generated_at=generated_at,
            prediction=prediction,
            advice=advice,
            strategy_names=strategy_names,
            stock_data=stock_data,
            stock_news=stock_news,
        )

        return {
            "generated_at": generated_at,
            "symbol": symbol,
            "market": market,
            "advice": advice,
            "prediction": {
                "direction": prediction.direction,
                "confidence": prediction.confidence,
                "reason": prediction.reason,
            },
            "strategy_names": strategy_names,
            "stock_data": stock_data,
            "stock_news": stock_news,
            "report_markdown": report_text,
            "report_html": report_html,
        }

    # Advice derivation method
    @staticmethod
    def _derive_advice(prediction: PredictionOutcome) -> str:
        return _ADVICE_BY_DIRECTION.get(prediction.direction, "HOLD")

    # Report saving and rendering methods
    @staticmethod
    def save_html_report(report: Dict[str, Any], output_path: Union[str, Path]) -> Path:
        """Writes ``report['report_html']`` to ``output_path`` and returns the path."""
        path = Path(output_path)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        path = path.resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report["report_html"], encoding="utf-8")
        return path

    # Markdown and HTML rendering methods
    @staticmethod
    def _render_markdown(
        symbol: str,
        market: str,
        generated_at: str,
        prediction: PredictionOutcome,
        advice: str,
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
                f"- Advice: {advice}",
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

    # HTML rendering method
    @staticmethod
    def _render_html(
        symbol: str,
        market: str,
        generated_at: str,
        prediction: PredictionOutcome,
        advice: str,
        strategy_names: List[str],
        stock_data: Dict[str, Any],
        stock_news: Dict[str, Any],
    ) -> str:
        history_count = len(stock_data.get("history", []))
        news_items = stock_news.get("news_items", [])
        sentiment_score = stock_news.get("sentiment_score", 0)

        advice_class = {"BUY": "advice-buy", "SELL": "advice-sell", "HOLD": "advice-hold"}.get(advice, "advice-hold")

        strategies_html = (
            "".join(f"<li>{html.escape(str(name))}</li>" for name in strategy_names)
            if strategy_names
            else "<li>none</li>"
        )

        news_rows = "".join(
            "<tr>"
            f"<td>{html.escape(str(item.get('title', '')))}</td>"
            f"<td>{html.escape(str(item.get('source', '')))}</td>"
            f"<td>{html.escape(str(item.get('published_at', '')))}</td>"
            "</tr>"
            for item in news_items[:10]
        )
        if not news_rows:
            news_rows = "<tr><td colspan=\"3\">No news items available.</td></tr>"

        template = HTML_TEMPLATE_PATH.read_text(encoding="utf-8")
        values = {
            "symbol": html.escape(symbol),
            "market": html.escape(market),
            "generated_at": html.escape(generated_at),
            "advice_class": advice_class,
            "advice": html.escape(advice),
            "direction": html.escape(prediction.direction),
            "confidence": f"{prediction.confidence:.0%}",
            "reason": html.escape(prediction.reason),
            "strategies_html": strategies_html,
            "history_count": str(history_count),
            "news_count": str(len(news_items)),
            "sentiment_score": html.escape(str(sentiment_score)),
            "news_rows": news_rows,
        }
        for name, value in values.items():
            template = template.replace(f"{{{{{name}}}}}", value)
        return template

# Demo usage of the AIReportAgent class
if __name__ == "__main__":
    demo_agent = AIReportAgent()

    demo_cases = [
        {
            "symbol": "AAPL",
            "market": "us",
            "prediction": PredictionOutcome(
                direction="up", confidence=0.8, reason="momentum + positive news"
            ),
            "strategy_names": ["ma_golden_cross", "volume_breakout", "bull_trend"],
            "stock_data": {"history": [{"close": 100}, {"close": 108}]},
            "stock_news": {
                "news_items": [
                    {"title": "Apple beats earnings", "source": "Reuters", "published_at": "2026-08-20"},
                ],
                "sentiment_score": 2,
            },
        },
        {
            "symbol": "AC",
            "market": "ca",
            "prediction": PredictionOutcome(
                direction="sideways", confidence=0.6, reason="range-bound price + mixed news"
            ),
            "strategy_names": ["box_oscillation", "shrink_pullback", "event_driven"],
            "stock_data": {"history": [{"close": 25.0}, {"close": 25.4}]},
            "stock_news": {
                "news_items": [
                    {
                        "title": "Air Canada updates full-year guidance",
                        "source": "Bloomberg",
                        "published_at": "2026-08-22",
                    },
                ],
                "sentiment_score": 0,
            },
        },
        {
            "symbol": "BB",
            "market": "us",
            "prediction": PredictionOutcome(
                direction="down", confidence=0.7, reason="weak momentum + negative news"
            ),
            "strategy_names": ["wave_theory", "growth_quality", "expectation_repricing"],
            "stock_data": {"history": [{"close": 5.2}, {"close": 4.9}]},
            "stock_news": {
                "news_items": [
                    {
                        "title": "BlackBerry misses revenue estimates",
                        "source": "CNBC",
                        "published_at": "2026-08-25",
                    },
                ],
                "sentiment_score": -1,
            },
        },
    ]

    for case in demo_cases:
        demo_report = demo_agent.build_report(**case)
        demo_path = AIReportAgent.save_html_report(
            demo_report, f"temps/ai_stock/ai_report_{case['symbol'].lower()}_demo.html"
        )
        print(
            f"symbol={case['symbol']} advice={demo_report['advice']} "
            f"report saved to {demo_path}"
        )
