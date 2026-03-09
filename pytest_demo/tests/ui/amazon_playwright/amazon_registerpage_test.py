import logging

import pytest

from pytest_demo.tests.ui.amazon_playwright.amazon_signinpage_test import goto_register_page

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.playwright
def test_registerpage_title(open_amazon_homepage_pw):
    logger.info("Verifying Amazon register page title (Playwright)")
    register_page = goto_register_page(open_amazon_homepage_pw)
    assert "Amazon" in register_page.title()
