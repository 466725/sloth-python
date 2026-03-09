import logging

import pytest

logger = logging.getLogger(__name__)
signin_button_id = "login"
signup_button_id = "menu_signup"


def goto_signup_page(open_tangerine_homepage_pw):
    logger.info("Navigating to Tangerine signup page (Playwright)")
    open_tangerine_homepage_pw.locator(f"#{signin_button_id}").click()
    open_tangerine_homepage_pw.locator(f"#{signup_button_id}").click()
    return open_tangerine_homepage_pw


@pytest.mark.ui
@pytest.mark.playwright
def test_signinpage_title(open_tangerine_homepage_pw):
    logger.info("Verifying Tangerine signin page title (Playwright)")
    open_tangerine_homepage_pw.locator(f"#{signin_button_id}").click()
    assert "Tangerine" in open_tangerine_homepage_pw.title()
