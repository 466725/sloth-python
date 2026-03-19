import logging

import pytest

from pytest_demo.tests.ui.tangerine_selenium.signinpage_test import goto_signup_page
from utils.config import settings

logger = logging.getLogger(__name__)


# Test Tangerine signup page begins here
@pytest.mark.ui
def test_signuppage_title(open_tangerine_homepage):
    logger.info("Verifying signup page title")
    signup_page = goto_signup_page(open_tangerine_homepage)
    signup_page.implicitly_wait(settings.selenium.implicit_wait)
    assert "Tangerine" in signup_page.title
