from __future__ import annotations

import logging
import os

import allure
import pytest

from utils.constants import TANGERINE_URL

logger = logging.getLogger(__name__)


def _headless_enabled() -> bool:
    return os.getenv("PW_HEADLESS", "1") != "0"


def _attach_page_screenshot(page, name: str) -> None:
    allure.attach(
        page.screenshot(full_page=True),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )

@pytest.fixture(scope="class")
def open_tangerine_homepage_pw(request: pytest.FixtureRequest):
    pw = pytest.importorskip("playwright.sync_api")
    with pw.sync_playwright() as p:
        browser = p.chromium.launch(headless=_headless_enabled())
        context = browser.new_context(locale="en-US")
        page = context.new_page()
        page.goto(TANGERINE_URL, wait_until="domcontentloaded")
        yield page
        _attach_page_screenshot(page, f"{request.node.name}-playwright")
        context.close()
        browser.close()