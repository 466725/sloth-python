import logging

import pytest

logger = logging.getLogger(__name__)


# Test Amazon homepage begins here
@pytest.mark.ui
def test_homepage_title(open_amazon_homepage):
    logger.info("Verifying homepage title")
    assert "Amazon" in open_amazon_homepage.title
