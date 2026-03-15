import logging

import pytest

logger = logging.getLogger(__name__)


# Test Tangerine homepage begins here
@pytest.mark.ui
def test_homepage_title(open_tangerine_homepage):
    logger.info("Verifying homepage title")
    assert "Tangerine" in open_tangerine_homepage.title
