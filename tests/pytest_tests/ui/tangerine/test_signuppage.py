import logging

import allure
import pytest

from ui.tangerine.test_signinpage import goto_signup_page

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.playwright
@allure.description("Owner: Weipeng Zheng")
def test_signuppage_title(tangerine_homepage):
    logger.info("Verifying Tangerine signup page title (Playwright)")
    signup_page = goto_signup_page(tangerine_homepage)
    assert "Tangerine" in signup_page.title()
