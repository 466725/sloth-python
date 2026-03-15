import logging

import pytest

from pytest_demo.self_healing.locator_store import get_locator
from pytest_demo.self_healing.self_healing import find_element

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.playwright
def test_homepage_title(tangerine_homepage):
    logger.info("Verifying Tangerine homepage title")
    find_element(tangerine_homepage, "tangerine.login", get_locator("tangerine.login"))
    assert "Tangerine" in tangerine_homepage.title()
