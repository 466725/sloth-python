import pytest


# Test Amazon homepage begins here
@pytest.mark.ui
def test_homepage(selenium):
    selenium.get("https://www.amazon.com/")
    assert True
