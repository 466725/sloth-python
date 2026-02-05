import pytest
from selenium.webdriver.common.by import By
from tenacity import sleep


def goto_register_page(open_homepage):
    open_homepage.find_element(By.ID, "nav-link-accountList").click()
    sleep(1)
    open_homepage.find_element(By.ID, "ab-registration-ingress-link").click()
    sleep(1)
    return open_homepage


# Test Amazon signin page begins here
@pytest.mark.ui
def test_signinpage_title(open_homepage):
    driver = open_homepage
    driver.find_element(By.ID, "nav-link-accountList").click()
    sleep(1)
    assert "Amazon Sign-In" in driver.title
