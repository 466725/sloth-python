from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.constants import SELENIUM_IMPLICITLY_WAIT, AMAZON_URL, SLEEP_TIME, TANGERINE_URL
from utils.screenshot_handler import ScreenshotHandler

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def project_root() -> Path:
    """
    Repository root directory.

    conftest.py lives in: <repo_root>/pytest_demo/conftest.py
    so parents[1] points to <repo_root>.
    """
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", name="pytest_demo_dir")
def demo_dir(project_root: Path) -> Path:
    """Path to the pytest_demo package directory."""
    return project_root / "pytest_demo"


@pytest.fixture(scope="session", autouse=True)
def _set_cwd_to_project_root(project_root: Path) -> None:
    """
    Make test runs stable regardless of where pytest is invoked from.

    This ensures code using paths like 'pytest_demo/calculator-data.csv'
    works consistently.
    """
    os.chdir(project_root)


@pytest.fixture(autouse=True)
def _print_before_after_each_test(request: pytest.FixtureRequest):
    """
    Runs around every single test:
    - before yield: setup / "before test"
    - after yield: teardown / "after test"
    """
    logger.info("\n----------------------Beginning of test--------------------------\n")
    sys.stdout.write(f"[BEFORE] {request.node.nodeid}\n")
    sys.stdout.flush()
    yield
    sys.stdout.write(f"\n[AFTER]  {request.node.nodeid}\n")
    logger.info("\n----------------------Ending of test--------------------------\n")
    sys.stdout.flush()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """
    Expose test outcome to fixtures via `request.node.rep_call`.
    This lets fixtures decide (in teardown) whether the test failed.
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.rep_call = rep


@pytest.fixture(scope="class")
def open_amazon_homepage(request: pytest.FixtureRequest):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--lang=en-US")

    driver = webdriver.Chrome(options=options)
    driver.get(AMAZON_URL)
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


@pytest.fixture(scope="class")
def open_tangerine_homepage(request: pytest.FixtureRequest):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--lang=en-US")

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
