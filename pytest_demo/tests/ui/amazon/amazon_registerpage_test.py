import pytest
from tenacity import sleep

from pytest_demo.tests.ui.amazon.amazon_signinpage_test import goto_register_page


# Test Amazon register page begins here
@pytest.mark.ui
def test_registerpage_title(open_homepage):
    driver = goto_register_page(open_homepage)
    sleep(1)
    driver.implicitly_wait(10)
    assert "Amazon Business" in driver.title
