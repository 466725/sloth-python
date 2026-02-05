import logging

import pytest

from pytest_demo.tests.ui.amazon.amazon_signinpage_test import goto_register_page
from utils.constants import SELENIUM_IMPLICITLY_WAIT

logger = logging.getLogger(__name__)


# Test Amazon register page begins here
@pytest.mark.ui
def test_registerpage_title(open_homepage):
    driver = goto_register_page(open_homepage)
    driver.implicitly_wait(SELENIUM_IMPLICITLY_WAIT)
    assert "Amazon Business" in driver.title
