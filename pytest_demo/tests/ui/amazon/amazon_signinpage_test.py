import logging

import pytest
from selenium.webdriver.common.by import By

from utils.constants import SELENIUM_IMPLICITLY_WAIT

logger = logging.getLogger(__name__)
account_list_link_id = "nav-link-accountList"
register_page_link_id = "ab-registration-ingress-link"


def goto_register_page(open_homepage):
    logger.info("Navigating to Amazon register page")
    account_list_link = open_homepage.find_element(By.ID, account_list_link_id)
    account_list_link.click()
    open_homepage.implicitly_wait(SELENIUM_IMPLICITLY_WAIT)
    open_homepage.find_element(By.ID, register_page_link_id).click()
    open_homepage.implicitly_wait(SELENIUM_IMPLICITLY_WAIT)
    return open_homepage


# Test Amazon signin page begins here
@pytest.mark.ui
def test_signinpage_title(open_homepage):
    logger.info("Verifying signin page title")
    signin_page = open_homepage
    account_list_link = signin_page.find_element(By.ID, account_list_link_id)
    account_list_link.click()
    signin_page.implicitly_wait(SELENIUM_IMPLICITLY_WAIT)
    assert "Amazon Sign-In" in signin_page.title
