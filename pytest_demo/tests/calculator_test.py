import pytest

from utils.csv_reader import read_csv_to_list


@pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (2, 3, 5)])
def test_add(a, b, expected):
    """Base test function for addition operation."""
    assert a + b == expected


@pytest.mark.ddt
@pytest.mark.parametrize("a,b,expected", read_csv_to_list("pytest_demo/tests/calculator-data.csv"))
def test_ddt(a, b, expected):
    assert a + b == expected
