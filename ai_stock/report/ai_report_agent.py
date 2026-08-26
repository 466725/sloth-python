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

    @staticmethod
    def _derive_advice(prediction: PredictionOutcome) -> str:
        return _ADVICE_BY_DIRECTION.get(prediction.direction, "HOLD")

    @staticmethod
    def save_html_report(report: Dict[str, Any], output_path: Union[str, Path]) -> Path:
        """Writes ``report['report_html']`` to ``output_path`` and returns the path."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report["report_html"], encoding="utf-8")
        return path

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

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Stock Report - {html.escape(symbol)}</title>
<style>
    :root {{
        --bg: #f9fafb;
        --text: #1f2937;
        --muted: #6b7280;
        --card-bg: #ffffff;
        --card-shadow: 0 1px 3px rgba(0,0,0,0.1);
        --border: #e5e7eb;
        --btn-bg: #f3f4f6;
        --btn-text: #111827;
        --btn-border: #d1d5db;
    }}

    body.dark-theme {{
        --bg: #111827;
        --text: #e5e7eb;
        --muted: #9ca3af;
        --card-bg: #1f2937;
        --card-shadow: 0 1px 3px rgba(0,0,0,0.45);
        --border: #374151;
        --btn-bg: #374151;
        --btn-text: #f9fafb;
        --btn-border: #4b5563;
    }}

    body {{
        font-family: Arial, Helvetica, sans-serif;
        margin: 2rem;
        color: var(--text);
        background: var(--bg);
        transition: background-color 0.2s ease, color 0.2s ease;
    }}

    .card {{
        background: var(--card-bg);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
        max-width: 720px;
        margin: 0 auto;
    }}

    .header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
    }}

    h1 {{ margin-top: 0; margin-bottom: 0.25rem; }}

    .theme-toggle {{
        border: 1px solid var(--btn-border);
        background: var(--btn-bg);
        color: var(--btn-text);
        border-radius: 6px;
        padding: 0.4rem 0.7rem;
        cursor: pointer;
        font-size: 0.85rem;
        white-space: nowrap;
    }}

  .advice {{ display: inline-block; padding: 0.5rem 1.25rem; border-radius: 6px; font-size: 1.5rem; font-weight: bold; color: #fff; }}
  .advice-buy {{ background: #16a34a; }}
  .advice-sell {{ background: #dc2626; }}
  .advice-hold {{ background: #d97706; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 0.5rem; }}
    th, td {{ text-align: left; padding: 0.4rem 0.5rem; border-bottom: 1px solid var(--border); font-size: 0.9rem; }}
    .meta {{ color: var(--muted); font-size: 0.9rem; }}
  ul {{ margin: 0.25rem 0 1rem 1.25rem; }}
</style>
</head>
<body>
  <div class="card">
        <div class="header">
            <h1>{html.escape(symbol)} <span class="meta">({html.escape(market)})</span></h1>
            <button id="theme-toggle" class="theme-toggle" type="button" aria-label="Toggle light and dark theme">
                🌙 Dark
            </button>
        </div>

    <p class="meta">Generated at (UTC): {html.escape(generated_at)}</p>
    <p><span class="advice {advice_class}">{html.escape(advice)}</span></p>
    <p><strong>Direction:</strong> {html.escape(prediction.direction)} &nbsp;
       <strong>Confidence:</strong> {prediction.confidence:.0%}</p>
    <p><strong>Reason:</strong> {html.escape(prediction.reason)}</p>

    <h2>Applied Strategies</h2>
    <ul>{strategies_html}</ul>

    <h2>Data Summary</h2>
    <ul>
      <li>History rows: {history_count}</li>
      <li>News items: {len(news_items)}</li>
      <li>News sentiment score: {html.escape(str(sentiment_score))}</li>
    </ul>

    <h2>Recent News</h2>
    <table>
      <thead><tr><th>Title</th><th>Source</th><th>Published</th></tr></thead>
      <tbody>{news_rows}</tbody>
    </table>
  </div>

    <script>
        (function () {{
            var storageKey = "ai_report_theme";
            var body = document.body;
            var btn = document.getElementById("theme-toggle");

            function applyTheme(theme) {{
                if (theme === "dark") {{
                    body.classList.add("dark-theme");
                    btn.textContent = "☀️ Light";
                }} else {{
                    body.classList.remove("dark-theme");
                    btn.textContent = "🌙 Dark";
                }}
            }}

            var savedTheme = localStorage.getItem(storageKey);
            if (!savedTheme) {{
                savedTheme = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
                    ? "dark"
                    : "light";
            }}
            applyTheme(savedTheme);

            btn.addEventListener("click", function () {{
                var nextTheme = body.classList.contains("dark-theme") ? "light" : "dark";
                applyTheme(nextTheme);
                localStorage.setItem(storageKey, nextTheme);
            }});
        }})();
    </script>
</body>
</html>
"""


if __name__ == "__main__":
    demo_agent = AIReportAgent()
    demo_report = demo_agent.build_report(
        symbol="AAPL",
        market="us",
        prediction=PredictionOutcome(direction="up", confidence=0.8, reason="momentum + positive news"),
        strategy_names=["ma_golden_cross"],
        stock_data={"history": [{"close": 100}, {"close": 108}]},
        stock_news={
            "news_items": [
                {"title": "Apple beats earnings", "source": "Reuters", "published_at": "2026-08-20"},
            ],
            "sentiment_score": 2,
        },
    )
    demo_path = AIReportAgent.save_html_report(demo_report, "temps/ai_report_demo.html")
    print(f"advice={demo_report['advice']} report saved to {demo_path}")
