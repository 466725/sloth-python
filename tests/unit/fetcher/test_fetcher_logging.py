import logging
import os
import sys
import types
import unittest
from unittest.mock import patch

import pandas as pd
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from ai_stock.stock_data.base import BaseFetcher, DataFetchError, DataFetcherManager
from ai_stock.stock_data.efinance_fetcher import EfinanceFetcher


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2026-03-06", "2026-03-07"],
            "open": [10.0, 10.2],
            "high": [10.5, 10.4],
            "low": [9.8, 10.1],
            "close": [10.3, 10.35],
            "volume": [1000, 1200],
            "amount": [10300, 12420],
            "pct_chg": [1.0, 0.49],
        }
    )


class _SuccessFetcher(BaseFetcher):
    name = "SuccessFetcher"
    priority = 1

    def _fetch_raw_data(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        return _sample_df()

    def _normalize_data(self, df: pd.DataFrame, stock_code: str) -> pd.DataFrame:
        return df


class _FailureFetcher(BaseFetcher):
    name = "FailureFetcher"
    priority = 0

    def _fetch_raw_data(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        raise DataFetchError(
            "Eastmoney 历史K线接口失败: "
            "endpoint=push2his.eastmoney.com/api/qt/stock/kline/get, "
            "category=remote_disconnect"
        )

    def _normalize_data(self, df: pd.DataFrame, stock_code: str) -> pd.DataFrame:
        return df


class _RecordingFetcher(BaseFetcher):
    def __init__(self, name: str, priority: int):
        self.name = name
        self.priority = priority
        self.calls = []

    def _fetch_raw_data(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        self.calls.append(stock_code)
        return _sample_df()

    def _normalize_data(self, df: pd.DataFrame, stock_code: str) -> pd.DataFrame:
        return df


class TestFetcherLogging(unittest.TestCase):
    @patch("ai_stock.stock_data.efinance_fetcher.get_config")
    def test_efinance_rejects_hk_daily_without_calling_eastmoney(self, mock_get_config):
        mock_get_config.return_value = types.SimpleNamespace(enable_eastmoney_patch=False)
        fetcher = EfinanceFetcher(sleep_min=0, sleep_max=0)

        with patch.object(fetcher, "_fetch_stock_data") as mock_fetch_stock_data:
            with self.assertRaises(DataFetchError) as captured:
                fetcher.get_daily_data("1211.HK", start_date="2026-05-01", end_date="2026-05-08")

        mock_fetch_stock_data.assert_not_called()
        self.assertIn("不支持港股日线", str(captured.exception))

    def test_efinance_logs_eastmoney_endpoint_on_remote_disconnect(self):
        fetcher = EfinanceFetcher()
        fake_efinance = types.SimpleNamespace(
            stock=types.SimpleNamespace(
                get_quote_history=lambda **kwargs: (_ for _ in ()).throw(
                    requests.exceptions.ConnectionError("Remote end closed connection without response")
                )
            )
        )

        with patch.dict(sys.modules, {"efinance": fake_efinance}):
            with patch.object(fetcher, "_set_random_user_agent", return_value=None), patch.object(
                fetcher, "_enforce_rate_limit", return_value=None
            ):
                with self.assertLogs(level="INFO") as captured:
                    with self.assertRaises(DataFetchError):
                        fetcher.get_daily_data("601006", start_date="2026-01-07", end_date="2026-03-08")

        log_text = "\n".join(captured.output)
        self.assertIn("Eastmoney 历史K线接口失败:", log_text)
        self.assertIn("endpoint=push2his.eastmoney.com/api/qt/stock/kline/get", log_text)
        self.assertIn("category=remote_disconnect", log_text)
        self.assertIn("[EfinanceFetcher] 601006 获取失败:", log_text)


if __name__ == "__main__":
    unittest.main()
