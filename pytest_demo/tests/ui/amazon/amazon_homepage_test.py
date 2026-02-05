import logging

import pytest
from pytest_selenium import driver

logger = logging.getLogger(__name__)
logger.info("Hello from a amazon_homepage_test.py file")

# Test Amazon homepage begins here
@pytest.mark.ui
def test_homepage_title(open_homepage):
    driver = open_homepage
    assert "Amazon" in driver.title