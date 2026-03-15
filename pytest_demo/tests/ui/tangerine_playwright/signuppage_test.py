import logging

import pytest

from pytest_demo.tests.ui.tangerine_playwright.signinpage_test import goto_signup_page

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.playwright
def test_signuppage_title(open_tangerine_homepage_pw):
    logger.info("Verifying Tangerine signup page title (Playwright)")
    signup_page = goto_signup_page(open_tangerine_homepage_pw)
    assert "Tangerine" in signup_page.title()
