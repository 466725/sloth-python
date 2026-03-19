from __future__ import annotations

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from utils.config import settings

ROBOT_LIBRARY_SCOPE = "GLOBAL"

_pw: Playwright | None = None
_browser: Browser | None = None
_context: BrowserContext | None = None
_page: Page | None = None


def open_browser_session() -> None:
    global _pw, _browser, _context, _page
    if _page is not None:
        return

    _pw = sync_playwright().start()
    _browser = _pw.chromium.launch(headless=settings.playwright.headless)
    _context = _browser.new_context(locale=settings.ui.locale)
    _page = _context.new_page()


def close_browser_session() -> None:
    global _pw, _browser, _context, _page
    if _page is not None:
        _page.screenshot(path="temps/playwright-robot-last.png", full_page=True)

    if _context is not None:
        _context.close()
    if _browser is not None:
        _browser.close()
    if _pw is not None:
        _pw.stop()

    _pw = None
    _browser = None
    _context = None
    _page = None


def open_tangerine_homepage() -> None:
    page = _require_page()
    page.goto(settings.ui.base_url, wait_until="domcontentloaded")
    accept_cookies_if_present()


def accept_cookies_if_present() -> None:
    page = _require_page()
    button = page.locator("#onetrust-accept-btn-handler").first
    if button.count() == 0:
        return
    if button.is_visible():
        button.click(timeout=5000)


def go_to_sign_in_page() -> None:
    page = _require_page()
    page.locator("#login").first.click(timeout=8000)


def go_to_sign_up_page() -> None:
    page = _require_page()
    page.locator("#login").first.click(timeout=8000)
    page.locator("#menu_signup").first.click(timeout=8000)


def page_title_should_contain(expected: str) -> None:
    page = _require_page()
    title = page.title()
    if expected not in title:
        raise AssertionError(f"Expected '{expected}' to be in page title, but got '{title}'.")


def _require_page() -> Page:
    if _page is None:
        raise RuntimeError("Browser session is not started. Call 'Open Browser Session' first.")
    return _page

