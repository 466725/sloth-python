import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.playwright
def test_homepage_title(open_amazon_homepage_pw):
    logger.info("Verifying Amazon homepage title (Playwright)")
    assert "Amazon" in open_amazon_homepage_pw.title()
