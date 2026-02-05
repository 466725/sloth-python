import logging

import allure
import pytest

from utils.csv_reader import read_csv_to_list

logger = logging.getLogger(__name__)
logger.info("Hello from a calculator_test.py file")

@allure.epic("EPIC-1")
@allure.feature("FEATURE-1")
@allure.story("STORY-1")
@allure.title("Test with Allure annotations")
@allure.severity(severity_level=2)
@pytest.mark.unit
@pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (2, 3, 5)])
def test_add(a, b, expected):
    """Base test function for addition operation."""
    logger.info(f"Testing addition with a={a}, b={b}")
    assert a + b == expected


@pytest.mark.ddt
@pytest.mark.unit
@pytest.mark.parametrize("a,b,expected", read_csv_to_list("pytest_demo/tests/calculator-data.csv"))
def test_ddt(a, b, expected):
    assert a + b == expected
