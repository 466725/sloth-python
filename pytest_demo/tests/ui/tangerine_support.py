from __future__ import annotations

import logging
from typing import Any

from utils.config import settings

logger = logging.getLogger(__name__)

COOKIE_ACCEPT_BUTTON_ID = "onetrust-accept-btn-handler"
COOKIE_ACCEPT_BUTTON_SELECTOR = f"#{COOKIE_ACCEPT_BUTTON_ID}"
COOKIE_BANNER_TIMEOUT_SECONDS = settings.ui.cookie_banner_timeout_seconds
COOKIE_BANNER_TIMEOUT_MS = COOKIE_BANNER_TIMEOUT_SECONDS * 1000


def open_tangerine_homepage_playwright(page: Any) -> None:
    """Open the Tangerine homepage and dismiss the cookie banner when present."""
    logger.info("Opening Tangerine homepage in Playwright")
    page.goto(settings.ui.base_url, wait_until="domcontentloaded")
    accept_tangerine_cookies_playwright(page)


def accept_tangerine_cookies_playwright(page: Any) -> None:
    """Accept the OneTrust cookie banner for Playwright sessions when it appears."""
    button = page.locator(COOKIE_ACCEPT_BUTTON_SELECTOR).first

    try:
        button.wait_for(state="visible", timeout=COOKIE_BANNER_TIMEOUT_MS)
    except Exception:
        logger.info("Tangerine cookie banner not displayed for Playwright session")
        return

    try:
        button.click(timeout=COOKIE_BANNER_TIMEOUT_MS)
        logger.info("Accepted Tangerine cookie banner in Playwright")
    except Exception as exc:
        logger.warning("Unable to accept Tangerine cookie banner in Playwright: %s", exc)


