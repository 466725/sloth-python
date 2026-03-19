import logging

import pytest
from selenium.webdriver.common.by import By

from utils.config import settings

logger = logging.getLogger(__name__)
signin_button_id = "login"
signup_button_id = "menu_signup"


def goto_signup_page(open_tangerine_homepage):
    logger.info("Navigating to Tangerine signup page")
    account_list_link = open_tangerine_homepage.find_element(By.ID, signin_button_id)
    account_list_link.click()
    open_tangerine_homepage.implicitly_wait(settings.selenium.implicit_wait)
    open_tangerine_homepage.find_element(By.ID, signup_button_id).click()
    open_tangerine_homepage.implicitly_wait(settings.selenium.implicit_wait)
    return open_tangerine_homepage


# Test Tangerine signin page begins here
@pytest.mark.ui
def test_signinpage_title(open_tangerine_homepage):
    logger.info("Verifying signin page title")
    signin_page = open_tangerine_homepage
    account_list_link = signin_page.find_element(By.ID, signin_button_id)
    account_list_link.click()
    signin_page.implicitly_wait(settings.selenium.implicit_wait)
    assert "Tangerine" in signin_page.title
