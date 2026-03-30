import logging

import pytest

from pytest_demo.self_healing.locator_store import get_locator
from pytest_demo.self_healing.self_healing import click

logger = logging.getLogger(__name__)


def goto_signup_page(tangerine_homepage):
    logger.info("Navigating to Tangerine signup page (Playwright)")
    click(tangerine_homepage, "tangerine.login", get_locator("tangerine.login"))
    click(tangerine_homepage, "tangerine.signup", get_locator("tangerine.signup"))
    return tangerine_homepage


@pytest.mark.ui
@pytest.mark.playwright
def test_signinpage_title(tangerine_homepage):
    logger.info("Verifying Tangerine signin page title (Playwright)")
    click(tangerine_homepage, "tangerine.login", get_locator("tangerine.login"))
    assert "Tangerine" in tangerine_homepage.title()
