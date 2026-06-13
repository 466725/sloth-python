import yfinance as yf
from datetime import datetime
from typing import Optional, List


class YFinanceHelper:
    """
    Utility class to demonstrate common yfinance usage:
    - Fetch ticker info
    - Download historical OHLCV data
    - Get dividends & splits
    - Retrieve options chain
    """

    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)

    # ---------------------------------------------------------
    # 1. Basic Company Info
    # ---------------------------------------------------------
    def get_info(self) -> dict:
        """Return general company info."""
        return self.ticker.info

    # ---------------------------------------------------------
    # 2. Historical Price Data
    # ---------------------------------------------------------
    def get_history(
            self,
            period: str = "1mo",
            interval: str = "1d",
            start: Optional[str] = None,
            end: Optional[str] = None,
    ):
        """
        Fetch OHLCV historical data.
        period examples: '1d', '5d', '1mo', '6mo', '1y', '5y', 'max'
        interval examples: '1m', '5m', '1h', '1d', '1wk'
        """
        return self.ticker.history(
            period=period,
            interval=interval,
            start=start,
            end=end
        )

    # ---------------------------------------------------------
    # 3. Dividends & Splits
    # ---------------------------------------------------------
    def get_dividends(self):
        """Return dividend history."""
        return self.ticker.dividends

    def get_splits(self):
        """Return stock split history."""
        return self.ticker.splits

    # ---------------------------------------------------------
    # 4. Options Chain
    # ---------------------------------------------------------
    def get_option_expirations(self) -> List[str]:
        """Return available option expiration dates."""
        return self.ticker.options

    def get_options_chain(self, expiration: str):
        """Return calls & puts for a given expiration date."""
        return self.ticker.option_chain(expiration)

    # ---------------------------------------------------------
    # 5. Multi‑Ticker Download
    # ---------------------------------------------------------
    @staticmethod
    def download_multiple(symbols: List[str], period="1mo"):
        """Download OHLCV data for multiple tickers."""
        return yf.download(symbols, period=period)
