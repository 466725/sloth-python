from random import Random

import pytest

import pytest_demo


@pytest.fixture()
def before_after(request: pytest.FixtureRequest):
    print("\n----------------------Beginning of test--------------------------")
    print(f"[BEFORE] {request.node.nodeid}")
    yield
    print(f"\n[AFTER]  {request.node.nodeid}")
    print("----------------------Ending of test--------------------------")


def test_base(before_after):
    """Base test function for pytest_demo integration."""
    rng = Random()
    intX = rng.randint(5, 9)
    print(f"Random integer generated: {intX}")
    assert intX > 7


@pytest.mark.xfail
def test_base_with_failure():
    """Base test function for pytest_demo integration with failure."""
    print("Executing test_base_with_failure")
    assert True


@pytest.mark.skip(reason="Skipping this test for demonstration purposes")
def test_base_with_skip():
    """Base test function for pytest_demo integration with skip."""

    pytest_demo.skip("Skipping this test for demonstration purposes")
