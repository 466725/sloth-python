from __future__ import annotations

import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROBOT_LIBRARY_SCOPE = "GLOBAL"

_driver = None


def open_browser_session() -> None:
    global _driver
    if _driver is not None:
        return

    # Check if running in CI with Selenium Grid
    remote_url = os.getenv("SELENIUM_REMOTE_URL")
    
    if remote_url:
        # Use Selenium Grid for CI
        options = webdriver.ChromeOptions()
        headless = os.getenv("SELENIUM_HEADLESS", "1") != "0"
        if headless:
            options.add_argument("--headless=new")
        try:
            _driver = webdriver.Remote(command_executor=remote_url, options=options)
            _driver.implicitly_wait(10)
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Selenium Grid at {remote_url}: {e}")
    else:
        # Use local Chrome for local testing
        options = webdriver.ChromeOptions()
        headless = os.getenv("SELENIUM_HEADLESS", "1") != "0"
        if headless:
            options.add_argument("--headless=new")
        
        # Additional options for CI environments to prevent crashes
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-web-resources")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--disable-background-networking")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        
        # Set window size
        options.add_argument("--window-size=1920,1080")
        
        try:
            _driver = webdriver.Chrome(options=options)
            _driver.implicitly_wait(10)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Chrome WebDriver: {e}")


def close_browser_session() -> None:
    global _driver
    if _driver is not None:
        try:
            _driver.save_screenshot("temps/selenium-robot-last.png")
        except Exception:
            pass
        _driver.quit()
        _driver = None


def open_tangerine_homepage() -> None:
    driver = _require_driver()
    driver.get("https://www.tangerine.ca/en/personal")
    accept_cookies_if_present()


def accept_cookies_if_present() -> None:
    driver = _require_driver()
    try:
        wait = WebDriverWait(driver, 5)
        cookie_button = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_button.click()
    except Exception:
        # Cookie button not found or not clickable, which is fine
        pass


def go_to_sign_in_page() -> None:
    driver = _require_driver()
    wait = WebDriverWait(driver, 8)
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login")))
    login_button.click()


def go_to_sign_up_page() -> None:
    driver = _require_driver()
    wait = WebDriverWait(driver, 8)
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login")))
    login_button.click()
    signup_button = wait.until(EC.element_to_be_clickable((By.ID, "menu_signup")))
    signup_button.click()


def page_title_should_contain(expected: str) -> None:
    driver = _require_driver()
    title = driver.title
    if expected not in title:
        raise AssertionError(f"Expected '{expected}' to be in page title, but got '{title}'.")


def _require_driver() -> webdriver.Chrome:
    if _driver is None:
        raise RuntimeError("Browser session is not started. Call 'Open Browser Session' first.")
    return _driver

