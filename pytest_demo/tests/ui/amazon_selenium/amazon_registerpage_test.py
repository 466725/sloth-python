import logging

import pytest

from pytest_demo.tests.ui.amazon_selenium.amazon_signinpage_test import goto_register_page
from utils.constants import SELENIUM_IMPLICITLY_WAIT, SLEEP_TIME

logger = logging.getLogger(__name__)


# Test Amazon register page begins here
@pytest.mark.ui
def test_registerpage_title(open_amazon_homepage):
    logger.info("Verifying register page title")
    register_page = goto_register_page(open_amazon_homepage)
    register_page.implicitly_wait(SELENIUM_IMPLICITLY_WAIT)
    assert "Amazon Business" in register_page.title
