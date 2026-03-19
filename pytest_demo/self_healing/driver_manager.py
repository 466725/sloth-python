from __future__ import annotations

from contextlib import contextmanager

from utils.config import settings


@contextmanager
def get_page(base_url: str, locale: str = "en-US"):
    pw_mod = __import__("playwright.sync_api", fromlist=["sync_playwright"])
    sync_playwright = pw_mod.sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=settings.playwright.headless)
        context = browser.new_context(locale=locale or settings.ui.locale)
        page = context.new_page()
        page.goto(base_url, wait_until="domcontentloaded")
        try:
            yield page
        finally:
            context.close()
            browser.close()
