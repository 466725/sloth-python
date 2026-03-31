import pytest

from robot_demo.calculator.calculator import CalculationError, Calculator


@pytest.mark.unit
def test_push_single_digit_updates_expression() -> None:
    calc = Calculator()
    assert calc.push_single_button("1") == "1"


@pytest.mark.unit
def test_slash_button_uses_integer_division_operator() -> None:
    calc = Calculator()
    calc.push_single_button("1")
    assert calc.push_single_button("/") == "1//"


@pytest.mark.unit
def test_equal_evaluates_expression() -> None:
    calc = Calculator()
    calc.push_single_button("1")
    calc.push_single_button("+")
    calc.push_single_button("2")
    assert calc.push_single_button("=") == "3"


@pytest.mark.unit
def test_clear_button_resets_expression() -> None:
    calc = Calculator()
    calc.push_single_button("1")
    assert calc.push_single_button("C") == ""


@pytest.mark.unit
def test_invalid_button_raises_calculation_error_with_exact_message() -> None:
    calc = Calculator()
    with pytest.raises(CalculationError, match=r"^Invalid button 'k'\.$"):
        calc.push_single_button("k")


@pytest.mark.unit
def test_invalid_expression_raises_calculation_error_with_exact_message() -> None:
    calc = Calculator()
    calc.push_single_button("1")
    calc.push_single_button("+")
    with pytest.raises(CalculationError, match=r"^Invalid expression\.$"):
        calc.push_single_button("=")


@pytest.mark.unit
def test_division_by_zero_raises_calculation_error_with_exact_message() -> None:
    calc = Calculator()
    calc.push_single_button("1")
    calc.push_single_button("/")
    calc.push_single_button("0")
    with pytest.raises(CalculationError, match=r"^Division by zero\.$"):
        calc.push_single_button("=")


@pytest.mark.unit
def test_sequential_button_presses_keep_state_consistent() -> None:
    calc = Calculator()
    for button in "12+3=":
        result = calc.push_single_button(button)
    assert result == "15"

    # Continue from previous result to verify state continuity.
    calc.push_single_button("+")
    calc.push_single_button("5")
    assert calc.push_single_button("=") == "20"

