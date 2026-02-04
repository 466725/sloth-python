# Demo of Allure and its annotations
import allure
import pytest


@allure.epic("EPIC-1")
@allure.feature("FEATURE-1")
@allure.story("STORY-1")
@allure.title("Test with Allure annotations")
@allure.severity(severity_level=2)
def test_allure():
    """Simple test with Allure annotations"""
    assert True


@pytest.mark.parametrize("param1,param2", [(2, 3), (1, 4)])
def test_allure_with_parametrize(param1, param2):
    """Test with parametrization and Allure annotations"""
    assert param1 + param2 == 5
