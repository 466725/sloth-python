from __future__ import annotations


try:
    from .calculator import CalculationError, Calculator
except ImportError:
    # Fallback for direct module execution from the calculator folder.
    from calculator import CalculationError, Calculator


class CalculatorLibrary:
    """
    Test library for testing *Calculator* business logic.
    Interacts with the calculator directly using its ``push`` method.
    """

    ROBOT_LIBRARY_SCOPE = "TEST CASE"

    def __init__(self) -> None:
        self._calc: Calculator = Calculator()
        self._result: str = ""

    def push_button(self, button: str) -> None:
        """
        Pushes the specified ``button``.
        Examples:
        | Push Button | 1 |
        | Push Button | C |
        """
        self._result = self._calc.push_single_button(button)

    def push_buttons(self, buttons: str) -> None:
        """
        Pushes the specified ``buttons``.
        Example:
        | Push Buttons | 1 + 2 = |
        | Push Buttons | 3 * 7 = |
        """
        for button in buttons.replace(" ", ""):
            self.push_button(button)

    def result_should_be(self, expected: str) -> None:
        """
        Verifies that the current result is ``expected``.
        Example:
        | Push Buttons     | 1 + 2 = |
        | Result Should Be | 3       |
        """
        if self._result != expected:
            raise AssertionError(f"{self._result} != {expected}")

    def should_cause_error(self, expression: str) -> str:
        """
        Verifies that calculating the given ``expression`` causes an error.
        Examples:
        | Should Cause Error | invalid            |                   |
        | ${error} =         | Should Cause Error | 1 / 0             |
        | Should Be Equal    | ${error}           | Division by zero. |
        """
        try:
            self.push_buttons(expression)
        except CalculationError as err:
            return str(err)
        else:
            raise AssertionError(f"'{expression}' should have caused an error.")