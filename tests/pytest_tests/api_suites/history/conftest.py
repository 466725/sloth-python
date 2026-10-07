"""Shared history fixtures: direct database seeding without calling other APIs."""

from __future__ import annotations

import json
from datetime import datetime, timedelta

import pytest

from ai_stock.storage import AnalysisHistory, DatabaseManager


def _raw_result(code: str, name: str) -> str:
    return json.dumps(
        {
            "code": code,
            "name": name,
            "sentiment_score": 72,
            "operation_advice": "逢低买入",
            "trend_prediction": "震荡上行",
            "analysis_summary": "成交量温和放大，趋势偏多。",
            "model_used": "gemini-2.0-flash",
            "action": "buy",
            "report_language": "zh",
        },
        ensure_ascii=False,
    )


@pytest.fixture
def seeded_history(db_manager: DatabaseManager) -> list[AnalysisHistory]:
    """Insert two analysis records and return them detached from the session."""
    created = datetime.now() - timedelta(days=1)
    rows = [
        AnalysisHistory(
            query_id="query-alpha",
            code="600519",
            name="贵州茅台",
            report_type="deep",
            sentiment_score=72,
            operation_advice="逢低买入",
            trend_prediction="震荡上行",
            analysis_summary="成交量温和放大，趋势偏多。",
            raw_result=_raw_result("600519", "贵州茅台"),
            news_content="[]",
            ideal_buy=1600.0,
            secondary_buy=1550.0,
            stop_loss=1480.0,
            take_profit=1800.0,
            created_at=created,
        ),
        AnalysisHistory(
            query_id="query-beta",
            code="000858",
            name="五粮液",
            report_type="market_review",
            sentiment_score=55,
            operation_advice="观望",
            trend_prediction="横盘整理",
            analysis_summary="量能不足，等待方向选择。",
            raw_result=_raw_result("000858", "五粮液"),
            news_content="[]",
            created_at=created + timedelta(hours=1),
        ),
    ]

    with db_manager.session_scope() as session:
        session.add_all(rows)
        session.flush()
        for row in rows:
            session.expunge(row)

    return rows
