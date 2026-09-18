"""
    Why Google blocks you (even with headers)

    Google detects non-browser traffic using many signals, not just User‑Agent:

        Missing cookies
        Missing JS execution
        No TLS fingerprint matching Chrome
        No prior browsing history
        Data‑center IP
        Repeated automated requests

    So instead of results, Google returns pages like:

        /sorry/
        Consent page
        CAPTCHA page
        “Unusual traffic detected”

    These pages do not contain <h3> search titles, so your parser correctly finds nothing.
"""

from typing import List

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

GOOGLE_SEARCH_URL = "https://www.google.com/search"
REQUEST_TIMEOUT = 5

# ✅ Change these values and just right-click → Run
SEARCH_QUERY = "Test automation with Python ~_~"
RESULT_LIMIT = 10

# CI-safe, stable User-Agent
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def create_session() -> requests.Session:
    """Create a requests session with retry and exponential backoff."""
    retry_strategy = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


def fetch_search_results(session: requests.Session, query: str) -> str:
    """Fetch raw HTML for a Google search query."""
    response = session.get(
        GOOGLE_SEARCH_URL,
        params={"q": query},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.text


def parse_titles(html: str) -> List[str]:
    """Parse search result titles from Google HTML."""
    soup = BeautifulSoup(html, "html.parser")

    titles: List[str] = []
    for h3 in soup.select("h3"):
        text = h3.get_text(strip=True)
        if text:
            titles.append(text)

    return titles


def main() -> None:
    print(f"Searching Google for: {SEARCH_QUERY!r}\n")

    session = create_session()

    try:
        html = fetch_search_results(session, SEARCH_QUERY)
        titles = parse_titles(html)

        if not titles:
            print("No results found (or request was blocked by Google).")
            return

        print("Top results:\n")

        for idx, title in enumerate(titles[:RESULT_LIMIT], start=1):
            print(f"{idx}. {title}")

    except requests.exceptions.RequestException as exc:
        print(f"Network error: {exc}")
    except Exception as exc:
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
