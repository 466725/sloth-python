# -*- coding: utf-8 -*-
"""RSI formula tests for StockTrendAnalyzer."""

import unittest

import pandas as pd

from ai_stock.stock_analyzer import StockTrendAnalyzer

REPORT_RSI_CLOSE = [
    10,
    11,
    12,
    11,
    13,
    12,
    14,
    15,
    13,
    16,
    17,
    15,
    18,
    19,
    17,
    20,
    21,
    19,
    22,
    23,
    21,
    24,
    25,
    23,
    26,
]


class StockAnalyzerRsiTestCase(unittest.TestCase):
    def test_calculate_rsi_uses_wilder_ema_for_report_periods(self) -> None:
        analyzer = StockTrendAnalyzer()
        df = pd.DataFrame({"close": REPORT_RSI_CLOSE})

        result = analyzer._calculate_rsi(df)
        latest = result.iloc[-1]

        self.assertAlmostEqual(float(latest["RSI_6"]), 69.01902761094098)
        self.assertAlmostEqual(float(latest["RSI_12"]), 68.1701033115944)
        self.assertAlmostEqual(float(latest["RSI_24"]), 68.04934582724741)



if __name__ == "__main__":
    unittest.main()
