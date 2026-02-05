import logging

import pytest

logger = logging.getLogger(__name__)


# Test Amazon homepage begins here
@pytest.mark.ui
def test_homepage_title(open_homepage):
    driver = open_homepage
    assert "Amazon" in driver.title
