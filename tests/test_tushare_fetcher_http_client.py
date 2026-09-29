# -*- coding: utf-8 -*-
"""Regression tests for TushareFetcher HTTP client initialization."""

import importlib.util
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from tests.litellm_stub import ensure_litellm_stub
from ai_stock.stock_data.tushare_fetcher import TushareFetcher, _TushareHttpClient

ensure_litellm_stub()

try:
    json_repair_available = importlib.util.find_spec("json_repair") is not None
except ValueError:
    json_repair_available = "json_repair" in sys.modules

if not json_repair_available and "json_repair" not in sys.modules:
    sys.modules["json_repair"] = MagicMock()


class TestTushareFetcherInit(unittest.TestCase):
    """Ensure fetcher initialization no longer depends on the tushare SDK package."""

    def test_init_builds_http_client_when_token_present(self) -> None:
        config = SimpleNamespace(tushare_token="demo-token")

        with patch("ai_stock.stock_data.tushare_fetcher.get_config", return_value=config):
            fetcher = TushareFetcher()

        self.assertIsInstance(fetcher._api, _TushareHttpClient)
        self.assertTrue(fetcher.is_available())
        self.assertEqual(fetcher.priority, -1)


if __name__ == "__main__":
    unittest.main()
