from __future__ import annotations

import logging
from typing import Any

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.constants import TANGERINE_URL

logger = logging.getLogger(__name__)

COOKIE_ACCEPT_BUTTON_ID = "onetrust-accept-btn-handler"
COOKIE_ACCEPT_BUTTON_SELECTOR = f"#{COOKIE_ACCEPT_BUTTON_ID}"
COOKIE_BANNER_TIMEOUT_SECONDS = 5
COOKIE_BANNER_TIMEOUT_MS = COOKIE_BANNER_TIMEOUT_SECONDS * 1000


def open_tangerine_homepage_playwright(page: Any) -> None:
    """Open the Tangerine homepage and dismiss the cookie banner when present."""
    logger.info("Opening Tangerine homepage in Playwright")
    page.goto(TANGERINE_URL, wait_until="domcontentloaded")
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


def open_tangerine_homepage_selenium(driver: Any) -> None:
    """Open the Tangerine homepage and dismiss the cookie banner when present."""
    logger.info("Opening Tangerine homepage in Selenium")
    driver.get(TANGERINE_URL)
    accept_tangerine_cookies_selenium(driver)


def accept_tangerine_cookies_selenium(driver: Any) -> None:
    """Accept the OneTrust cookie banner for Selenium sessions when it appears."""
    wait = WebDriverWait(driver, COOKIE_BANNER_TIMEOUT_SECONDS)

    try:
        button = wait.until(EC.element_to_be_clickable((By.ID, COOKIE_ACCEPT_BUTTON_ID)))
    except TimeoutException:
        logger.info("Tangerine cookie banner not displayed for Selenium session")
        return

    try:
        button.click()
        logger.info("Accepted Tangerine cookie banner in Selenium")
    except WebDriverException as exc:
        logger.warning(
            "Selenium native click failed for Tangerine cookie banner. Falling back to JavaScript: %s",
            exc,
        )
        driver.execute_script("arguments[0].click();", button)

