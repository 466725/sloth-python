import logging

import pytest

from pytest_demo.self_healing.locator_store import get_locator
from pytest_demo.self_healing.self_healing import find_element

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.playwright
def test_homepage_title(open_amazon_homepage_pw):
    logger.info("Verifying Amazon homepage title (Playwright)")
    find_element(open_amazon_homepage_pw, "amazon.account_list", get_locator("amazon.account_list"))
    assert "Amazon" in open_amazon_homepage_pw.title()
