# -*- coding: utf-8 -*-
"""Tests that market-index retrieval rejects unsupported regions."""

import unittest

from ai_stock.stock_data.base import DataFetchError
from ai_stock.stock_data.yfinance_fetcher import YfinanceFetcher


class TestYfinanceMarketRegions(unittest.TestCase):
    def setUp(self):
        self.fetcher = YfinanceFetcher()

    def test_rejects_unsupported_market_regions(self):
        for region in ("hk", "jp", "kr"):
            with self.subTest(region=region), self.assertRaises(DataFetchError):
                self.fetcher.get_main_indices(region=region)


if __name__ == "__main__":
    unittest.main()
