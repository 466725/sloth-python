import logging

import pytest

from pytest_demo.self_healing.locator_store import get_locator
from pytest_demo.self_healing.self_healing import find_element

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.playwright
def test_homepage_title(open_tangerine_homepage_pw):
    logger.info("Verifying Tangerine homepage title (Playwright)")
    find_element(open_tangerine_homepage_pw, "tangerine.login", get_locator("tangerine.login"))
    assert "Tangerine" in open_tangerine_homepage_pw.title()
