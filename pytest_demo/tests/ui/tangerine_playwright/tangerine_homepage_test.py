import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.playwright
def test_homepage_title(open_tangerine_homepage_pw):
    logger.info("Verifying Tangerine homepage title (Playwright)")
    assert "Tangerine" in open_tangerine_homepage_pw.title()
