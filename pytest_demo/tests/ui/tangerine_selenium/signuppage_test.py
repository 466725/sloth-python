import logging

import pytest

from pytest_demo.tests.ui.tangerine_selenium.signinpage_test import goto_signup_page
from utils.constants import SELENIUM_IMPLICITLY_WAIT

logger = logging.getLogger(__name__)


# Test Tangerine signup page begins here
@pytest.mark.ui
def test_signuppage_title(open_tangerine_homepage):
    logger.info("Verifying signup page title")
    signup_page = goto_signup_page(open_tangerine_homepage)
    signup_page.implicitly_wait(SELENIUM_IMPLICITLY_WAIT)
    assert "Tangerine" in signup_page.title
