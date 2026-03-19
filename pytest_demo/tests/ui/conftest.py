from __future__ import annotations

import logging

import allure
import pytest

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pytest_demo.tests.ui.tangerine_support import (
    open_tangerine_homepage_playwright,
    open_tangerine_homepage_selenium,
)
from utils.config import settings
from utils.screenshot_handler import ScreenshotHandler

logger = logging.getLogger(__name__)


def _attach_page_screenshot(page, name: str) -> None:
    allure.attach(
        page.screenshot(full_page=True),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


@pytest.fixture(scope="function")
def tangerine_homepage(request: pytest.FixtureRequest):
    pw = pytest.importorskip("playwright.sync_api")
    with pw.sync_playwright() as p:
        browser = p.chromium.launch(headless=settings.playwright.headless)
        context = browser.new_context(locale=settings.ui.locale)
        page = context.new_page()
        open_tangerine_homepage_playwright(page)
        yield page
        _attach_page_screenshot(page, f"{request.node.name}-playwright")
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def open_tangerine_homepage(request: pytest.FixtureRequest):
    options = Options()
    for argument in settings.selenium.common_arguments:
        options.add_argument(argument)

    selenium_url = settings.selenium.remote_url
    if selenium_url:
        driver = webdriver.Remote(command_executor=selenium_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(settings.selenium.implicit_wait)
    open_tangerine_homepage_selenium(driver)
    sleep(settings.ui.sleep_time)

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
