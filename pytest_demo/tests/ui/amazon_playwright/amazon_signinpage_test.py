import logging

import pytest

from pytest_demo.self_healing.locator_store import get_locator
from pytest_demo.self_healing.self_healing import click

logger = logging.getLogger(__name__)


def goto_register_page(open_amazon_homepage_pw):
    logger.info("Navigating to Amazon register page (Playwright)")
    click(open_amazon_homepage_pw, "amazon.account_list", get_locator("amazon.account_list"))
    click(open_amazon_homepage_pw, "amazon.register_link", get_locator("amazon.register_link"))
    return open_amazon_homepage_pw


@pytest.mark.ui
@pytest.mark.playwright
def test_signinpage_title(open_amazon_homepage_pw):
    logger.info("Verifying Amazon signin page title (Playwright)")
    click(open_amazon_homepage_pw, "amazon.account_list", get_locator("amazon.account_list"))
    assert "Amazon Sign-In" in open_amazon_homepage_pw.title()
