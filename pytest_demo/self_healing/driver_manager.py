from __future__ import annotations

import os
from contextlib import contextmanager


@contextmanager
def get_page(base_url: str, locale: str = "en-US"):
    pw_mod = __import__("playwright.sync_api", fromlist=["sync_playwright"])
    sync_playwright = pw_mod.sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=os.getenv("PW_HEADLESS", "1") != "0")
        context = browser.new_context(locale=locale)
        page = context.new_page()
        page.goto(base_url, wait_until="domcontentloaded")
        try:
            yield page
        finally:
            context.close()
            browser.close()
