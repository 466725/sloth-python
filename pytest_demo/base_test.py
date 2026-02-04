import pytest

import pytest_demo


def test_base():
    """Base test function for pytest_demo integration."""

    assert True


def test_base_with_success():
    """Base test function for pytest_demo integration with success."""

    assert True


@pytest.mark.xfail
def test_base_with_failure():
    """Base test function for pytest_demo integration with failure."""

    assert False


@pytest.mark.skip(reason="Skipping this test for demonstration purposes")
def test_base_with_skip():
    """Base test function for pytest_demo integration with skip."""

    pytest_demo.skip("Skipping this test for demonstration purposes")


@pytest.mark.xfail
def test_base_with_xfail():
    """Base test function for pytest_demo integration with expected failure."""

    pytest_demo.xfail("Expected failure for demonstration purposes")


def test_base_with_success_and_assert():
    """Base test function for pytest_demo integration with success and assert."""

    assert True
