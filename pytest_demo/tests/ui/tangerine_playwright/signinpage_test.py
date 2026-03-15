import logging

import pytest

from pytest_demo.self_healing.locator_store import get_locator
from pytest_demo.self_healing.self_healing import click

logger = logging.getLogger(__name__)


def goto_signup_page(open_tangerine_homepage_pw):
    logger.info("Navigating to Tangerine signup page (Playwright)")
    click(open_tangerine_homepage_pw, "tangerine.login", get_locator("tangerine.login"))
    click(open_tangerine_homepage_pw, "tangerine.signup", get_locator("tangerine.signup"))
    return open_tangerine_homepage_pw


@pytest.mark.ui
@pytest.mark.playwright
def test_signinpage_title(open_tangerine_homepage_pw):
    logger.info("Verifying Tangerine signin page title (Playwright)")
    click(open_tangerine_homepage_pw, "tangerine.login", get_locator("tangerine.login"))
    assert "Tangerine" in open_tangerine_homepage_pw.title()
