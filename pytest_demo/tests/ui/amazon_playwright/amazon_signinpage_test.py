import logging

import pytest

logger = logging.getLogger(__name__)
account_list_link_id = "nav-link-accountList"
register_page_link_id = "ab-registration-ingress-link"


def goto_register_page(open_amazon_homepage_pw):
    logger.info("Navigating to Amazon register page (Playwright)")
    open_amazon_homepage_pw.locator(f"#{account_list_link_id}").click()
    open_amazon_homepage_pw.locator(f"#{register_page_link_id}").click()
    return open_amazon_homepage_pw


@pytest.mark.ui
@pytest.mark.playwright
def test_signinpage_title(open_amazon_homepage_pw):
    logger.info("Verifying Amazon signin page title (Playwright)")
    open_amazon_homepage_pw.locator(f"#{account_list_link_id}").click()
    assert "Amazon Sign-In" in open_amazon_homepage_pw.title()
