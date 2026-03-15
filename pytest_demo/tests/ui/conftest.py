from __future__ import annotations

import logging
import os

import allure
import pytest

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.constants import SELENIUM_IMPLICITLY_WAIT, SLEEP_TIME, TANGERINE_URL
from utils.screenshot_handler import ScreenshotHandler

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
def tangerine_homepage(request: pytest.FixtureRequest):
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


@pytest.fixture(scope="class")
def open_tangerine_homepage(request: pytest.FixtureRequest):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--lang=en-US")

    selenium_url = os.getenv("SELENIUM_REMOTE_URL")
    if selenium_url:
        driver = webdriver.Remote(command_executor=selenium_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.get(TANGERINE_URL)
    driver.implicitly_wait(SELENIUM_IMPLICITLY_WAIT)
    sleep(SLEEP_TIME)

    yield driver

    # Attach screenshot only if the test failed
    # rep = getattr(request.node, "rep_call", None)
    # if rep is not None and rep.failed:
    #     handler = ScreenshotHandler(driver)
    #     handler.attach_screenshot(name=f"{request.node.name}-failure")

    # Attach a screenshot regardless of the test outcome
    handler = ScreenshotHandler(driver)
    handler.attach_screenshot(name=f"{request.node.name}")

    driver.quit()
