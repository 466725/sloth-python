from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tenacity import sleep


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
    sys.stdout.write("\n----------------------Beginning of test--------------------------\n")
    sys.stdout.write(f"[BEFORE] {request.node.nodeid}\n")
    sys.stdout.flush()
    yield
    sys.stdout.write(f"\n[AFTER]  {request.node.nodeid}\n")
    sys.stdout.write("----------------------Ending of test--------------------------\n")
    sys.stdout.flush()


@pytest.fixture(scope="class")
def open_homepage():
    sys.stdout.write("\n----------------------Beginning of Amazon homepage test--------------------------\n")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.amazon.com/")
    sleep(1)
    driver.implicitly_wait(10)
    sys.stdout.flush()
    yield driver
    driver.quit()
    sys.stdout.write("----------------------Ending of Amazon homepage test--------------------------\n")
    sys.stdout.flush()
