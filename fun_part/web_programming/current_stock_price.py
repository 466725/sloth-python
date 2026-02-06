import requests
from bs4 import BeautifulSoup


def stock_price(symbol: str = "AAPL") -> str:
    url = f"https://finance.yahoo.com/quote/{symbol}"
    # Adding a User-Agent header to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Yahoo Finance uses 'fin-streamer' for live prices. 
        # This is more reliable than specific CSS layout classes.
        price_field = soup.find("fin-streamer", {"data-symbol": symbol.upper(), "data-field": "regularMarketPrice"})
        
        if price_field:
            return price_field.text
        return "Price not found"
        
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    for symbol in "AAPL AMZN IBM GOOG MSFT ORCL".split():
        print(f"Current {symbol:<4} stock price is {stock_price(symbol):>8}")
