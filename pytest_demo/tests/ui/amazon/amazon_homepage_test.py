import pytest
from pytest_selenium import driver


# Test Amazon homepage begins here
@pytest.mark.ui
def test_homepage_title(open_homepage):
    driver = open_homepage
    assert "" in driver.title