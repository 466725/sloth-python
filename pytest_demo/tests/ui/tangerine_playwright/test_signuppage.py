import logging

import pytest

from pytest_demo.tests.ui.tangerine_playwright.test_signinpage import goto_signup_page

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.playwright
def test_signuppage_title(tangerine_homepage):
    logger.info("Verifying Tangerine signup page title (Playwright)")
    signup_page = goto_signup_page(tangerine_homepage)
    assert "Tangerine" in signup_page.title()
