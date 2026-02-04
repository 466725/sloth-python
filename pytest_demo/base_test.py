from random import Random

import allure
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
    assert intX > 3


@pytest.mark.skip(reason="Skipping this test for demonstration purposes")
def test_base_with_skip():
    """Base test function for pytest_demo integration with skip."""

    pytest_demo.skip("Skipping this test for demonstration purposes")


@allure.epic("EPIC-1")
@allure.feature("FEATURE-1")
@allure.story("STORY-1")
@allure.title("Test with Allure annotations")
@allure.severity(severity_level=2)
@pytest.mark.parametrize("param1,param2", [(2, 3), (1, 4)])
def test_allure_with_parametrize(param1, param2):
    """Test with parametrization and Allure annotations"""
    assert param1 + param2 == 5
