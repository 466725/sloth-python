import logging

import pytest
from selenium.webdriver.common.by import By
from tenacity import sleep

logger = logging.getLogger(__name__)
logger.info("Hello from a amazon_signinpage_test.py file")


def goto_register_page(open_homepage):
    logger.info("Navigating to Amazon register page")
    open_homepage.find_element(By.ID, "nav-link-accountList").click()
    sleep(1)
    open_homepage.implicitly_wait(10)
    open_homepage.find_element(By.ID, "ab-registration-ingress-link").click()
    sleep(1)
    open_homepage = open_homepage
    open_homepage.implicitly_wait(10)
    return open_homepage


# Test Amazon signin page begins here
@pytest.mark.ui
def test_signinpage_title(open_homepage):
    driver = open_homepage
    driver.find_element(By.ID, "nav-link-accountList").click()
    sleep(1)
    driver.implicitly_wait(10)
    assert "Amazon Sign-In" in driver.title
