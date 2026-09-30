# -*- coding: utf-8 -*-
"""
Regression tests for provider-side A-share stock code conversion.
"""

import unittest

import pandas as pd

from ai_stock.stock_data.base import DataFetcherManager, normalize_stock_code
from ai_stock.stock_data.tushare_fetcher import TushareFetcher


class _RecordingDailyFetcher:
    name = "RecordingDailyFetcher"
    priority = 1

    def __init__(self) -> None:
        self.calls = []

    def get_daily_data(self, stock_code: str, *args, **kwargs) -> pd.DataFrame:
        self.calls.append(stock_code)
        return pd.DataFrame({"date": ["2026-05-22"], "close": [10.0]})


class TestDataFetcherManagerAShareCodes(unittest.TestCase):
    def test_get_daily_data_keeps_user_contract_as_bare_stock_code(self) -> None:
        fetcher = _RecordingDailyFetcher()
        manager = DataFetcherManager(fetchers=[fetcher])

        df, source = manager.get_daily_data("601888", days=1)

        self.assertFalse(df.empty)
        self.assertEqual(source, "RecordingDailyFetcher")
        self.assertEqual(fetcher.calls, ["601888"])

class TestTushareAShareCodeConversion(unittest.TestCase):
    def test_convert_bare_stock_codes_to_tushare_format(self) -> None:
        fetcher = TushareFetcher()

        self.assertEqual(fetcher._convert_stock_code("605499"), "605499.SH")
        self.assertEqual(fetcher._convert_stock_code("001979"), "001979.SZ")
        self.assertEqual(fetcher._convert_stock_code("003816"), "003816.SZ")
        self.assertEqual(fetcher._convert_stock_code("301012"), "301012.SZ")

    def test_convert_prefix_code_preserves_explicit_exchange_hint(self) -> None:
        fetcher = TushareFetcher()

        self.assertEqual(fetcher._convert_stock_code("SH000001"), "000001.SH")
        self.assertEqual(fetcher._convert_stock_code("SH.000001"), "000001.SH")
        self.assertEqual(fetcher._convert_stock_code("SZ600519"), "600519.SZ")
        self.assertEqual(fetcher._convert_stock_code("SZ.600519"), "600519.SZ")
        self.assertEqual(fetcher._convert_stock_code("ss.600519"), "600519.SH")


class TestNormalizeStockCode(unittest.TestCase):
    def test_normalize_prefixed_dot_code(self) -> None:
        self.assertEqual(normalize_stock_code("SH.600519"), "600519")
        self.assertEqual(normalize_stock_code("sh.600519"), "600519")
        self.assertEqual(normalize_stock_code("SZ.000001"), "000001")
        self.assertEqual(normalize_stock_code("sz.000001"), "000001")
        self.assertEqual(normalize_stock_code("BJ.920748"), "920748")


if __name__ == "__main__":
    unittest.main()
