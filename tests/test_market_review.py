# -*- coding: utf-8 -*-
"""Tests for localized market review wrappers."""

import importlib
import json
import os
import sys
import tempfile
import unittest
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock, patch

from market_analyzer import MarketAnalyzer
from tests.litellm_stub import ensure_litellm_stub

ensure_litellm_stub()

def _build_optional_module_stubs() -> dict[str, ModuleType]:
    stubs: dict[str, ModuleType] = {}
    google_module: ModuleType | None = None

    for module_name in ("google.generativeai", "google.genai", "anthropic"):
        try:
            importlib.import_module(module_name)
            continue
        except ImportError:
            stub = ModuleType(module_name)
            stubs[module_name] = stub
            if not module_name.startswith("google."):
                continue
            if google_module is None:
                try:
                    google_module = importlib.import_module("google")
                except ImportError:
                    google_module = ModuleType("google")
                    stubs["google"] = google_module
            setattr(google_module, module_name.split(".", 1)[1], stub)

    return stubs


sys.modules.update(_build_optional_module_stubs())
import ai_stock.core.market_review as market_review_module
from ai_stock.config import Config, get_config
from ai_stock.services.run_diagnostics import activate_run_diagnostic_context, reset_run_diagnostic_context
from ai_stock.storage import AnalysisHistory, DatabaseManager

run_market_review = market_review_module.run_market_review


class MarketReviewLocalizationTestCase(unittest.TestCase):
    def _make_notifier(self) -> MagicMock:
        notifier = MagicMock()
        notifier.save_report_to_file.return_value = "/tmp/market_review.md"
        notifier.is_available.return_value = True
        notifier.send.return_value = True
        return notifier

    def test_resolve_market_review_regions_returns_ordered_non_empty_list(self) -> None:
        cases = [
            (None, ["cn"]),
            ("", ["cn"]),
            ("both", ["cn", "hk", "us"]),
            (" CN,US,cn ", ["cn", "us"]),
            ("us,cn,us", ["cn", "us"]),
            ("eu,apac", ["cn"]),
            (",,", ["cn"]),
            ("HK", ["hk"]),
            ("invalid", ["cn"]),
        ]

        for raw_region, expected in cases:
            with self.subTest(raw_region=raw_region):
                self.assertEqual(
                    market_review_module._resolve_market_review_regions(raw_region),
                    expected,
                )

    def test_render_market_review_payload_markdown_does_not_repeat_title(self) -> None:
        markdown = market_review_module._render_market_review_payload_markdown(
            {
                "title": "2026-06-03 大盘复盘",
                "sections": [
                    {
                        "key": "daily_review",
                        "title": "2026-06-03 大盘复盘",
                        "markdown": "> 今日指数强弱分化。\n\n### 一、盘面总览\n正文",
                    }
                ],
            },
            wrapper_title="🎯 大盘复盘",
        )

        self.assertEqual(markdown.count("2026-06-03 大盘复盘"), 1)
        self.assertTrue(markdown.startswith("🎯 大盘复盘\n\n## 2026-06-03 大盘复盘"))

    def test_persist_market_review_history_saves_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            old_db_path = os.environ.get("DATABASE_PATH")
            os.environ["DATABASE_PATH"] = os.path.join(temp_dir, "market_review_history.db")
            Config._instance = None
            DatabaseManager.reset_instance()
            try:
                saved = market_review_module._persist_market_review_history(
                    review_report="## 今日大盘\n\n复盘正文",
                    markdown_report="# 🎯 大盘复盘\n\n## 今日大盘\n\n复盘正文",
                    region="cn",
                    config=SimpleNamespace(report_language="zh"),
                    query_id="market-task-001",
                    market_light_snapshots={
                        "cn": {
                            "region": "cn",
                            "trade_date": "2026-03-06",
                            "status": "red",
                            "score": 30,
                            "label": "偏防守",
                            "temperature_label": "偏弱",
                            "reasons": ["test"],
                            "guidance": "test",
                            "dimensions": {
                                "breadth": {"score": 20, "available": True},
                                "index": {"score": 30, "available": True},
                                "limit": {"score": 10, "available": True},
                            },
                            "data_quality": "ok",
                        }
                    },
                    market_review_payload={
                        "version": 1,
                        "kind": "market_review",
                        "region": "cn",
                        "sections": [{"title": "今日大盘", "markdown": "复盘正文"}],
                    },
                )

                self.assertGreater(saved, 0)
                db = DatabaseManager.get_instance()
                with db.get_session() as session:
                    row = session.query(AnalysisHistory).filter(
                        AnalysisHistory.query_id == "market-task-001"
                    ).first()
                    self.assertIsNotNone(row)
                    self.assertEqual(row.id, saved)
                    self.assertEqual(row.code, market_review_module.MARKET_REVIEW_HISTORY_CODE)
                    self.assertEqual(row.name, "大盘复盘")
                    self.assertEqual(row.report_type, market_review_module.MARKET_REVIEW_REPORT_TYPE)
                    self.assertEqual(row.news_content, "## 今日大盘\n\n复盘正文")
                    self.assertIn("# 🎯 大盘复盘", row.raw_result)
                    self.assertIn('"market_light_snapshots"', row.context_snapshot)
                    self.assertIn('"market_review_payload"', row.context_snapshot)
                    self.assertIn('"trade_date": "2026-03-06"', row.context_snapshot)
                    snapshot = json.loads(row.context_snapshot or "{}")
                    self.assertIn("analysis_context_pack_overview", snapshot)
            finally:
                DatabaseManager.reset_instance()
                Config._instance = None
                if old_db_path is None:
                    os.environ.pop("DATABASE_PATH", None)
                else:
                    os.environ["DATABASE_PATH"] = old_db_path

if __name__ == "__main__":
    unittest.main()
