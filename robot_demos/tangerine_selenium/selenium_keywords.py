from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import settings

ROBOT_LIBRARY_SCOPE = "GLOBAL"

_driver = None


def open_browser_session() -> None:
    global _driver
    if _driver is not None:
        return

    remote_url = settings.selenium.remote_url
    options = webdriver.ChromeOptions()
    for argument in settings.selenium.common_arguments:
        options.add_argument(argument)
    
    if remote_url:
        if settings.selenium.headless:
            options.add_argument("--headless=new")
        try:
            _driver = webdriver.Remote(command_executor=remote_url, options=options)
            _driver.implicitly_wait(settings.selenium.implicit_wait)
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Selenium Grid at {remote_url}: {e}")
    else:
        if settings.selenium.headless:
            options.add_argument("--headless=new")
        for argument in settings.selenium.stability_arguments:
            options.add_argument(argument)
        
        try:
            _driver = webdriver.Chrome(options=options)
            _driver.implicitly_wait(settings.selenium.implicit_wait)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Chrome WebDriver: {e}")


def close_browser_session() -> None:
    global _driver
    if _driver is not None:
        driver = _driver
        try:
            driver.save_screenshot("temps/selenium-robot-last.png")
        except Exception:
            pass
        driver.quit()
        _driver = None


def open_tangerine_homepage() -> None:
    driver = _require_driver()
    driver.get(settings.ui.base_url)
    accept_cookies_if_present()


def accept_cookies_if_present() -> None:
    driver = _require_driver()
    try:
        wait = WebDriverWait(driver, settings.ui.cookie_banner_timeout_seconds)
        cookie_button = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_button.click()
    except Exception:
        # Cookie button not found or not clickable, which is fine
        pass


def go_to_sign_in_page() -> None:
    driver = _require_driver()
    wait = WebDriverWait(driver, settings.selenium.explicit_wait)
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login")))
    login_button.click()


def go_to_sign_up_page() -> None:
    driver = _require_driver()
    wait = WebDriverWait(driver, settings.selenium.explicit_wait)
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

