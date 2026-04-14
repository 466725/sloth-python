from typing import Optional

import requests
from bs4 import BeautifulSoup
from requests import Session
from requests.exceptions import RequestException

YAHOO_FINANCE_URL = "https://finance.yahoo.com/quote/{symbol}"
REQUEST_TIMEOUT = 10

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def create_session() -> Session:
    """Create a reusable HTTP session."""
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def fetch_stock_price(session: Session, symbol: str) -> Optional[str]:
    """
    Fetch the current stock price for a symbol from Yahoo Finance.

    Returns:
        Stock price as string if found, otherwise None.
    """
    url = YAHOO_FINANCE_URL.format(symbol=symbol.upper())

    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except RequestException as exc:
        print(f"[ERROR] Failed to fetch {symbol}: {exc}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    price_tag = soup.find(
        "fin-streamer",
        {
            "data-symbol": symbol.upper(),
            "data-field": "regularMarketPrice",
        },
    )

    if price_tag and price_tag.text:
        return price_tag.text.strip()

    print(f"[WARN] Price not found for {symbol}")
    return None


def main() -> None:
    symbols = ["AAPL", "AMZN", "IBM", "GOOG", "MSFT", "ORCL"]

    session = create_session()

    for symbol in symbols:
        price = fetch_stock_price(session, symbol)
        display_price = price if price else "N/A"
        print(f"Current {symbol:<4} stock price is {display_price:>8}")


if __name__ == "__main__":
    main()
