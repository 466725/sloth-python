"""Website imports must not depend on the retired messaging bot package."""

import subprocess
import sys
from pathlib import Path


def test_web_backend_imports_without_bot() -> None:
    root = Path(__file__).resolve().parents[3]
    code = """
import sys
sys.modules["bot"] = None
from tests.unit.llm.litellm_stub import ensure_litellm_stub
ensure_litellm_stub()
from ai_stock.core.pipeline import StockAnalysisPipeline
from ai_stock.report.notification import NotificationService
from api.app import create_app
assert StockAnalysisPipeline
assert NotificationService
assert create_app
paths = create_app().openapi()["paths"]
assert "/api/v1/analysis/analyze" in paths
assert "/api/v1/agent/chat" in paths
assert "/api/v1/alerts/rules" in paths
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
