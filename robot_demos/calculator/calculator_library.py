from calculator import CalculationError, Calculator


class CalculatorLibrary:
    """Test library for testing *Calculator* business logic.

    Interacts with the calculator directly using its ``push`` method.
    """

    def __init__(self):
        self._calc = Calculator()
        self._result = ""

    def push_button(self, button):
        """Pushes the specified ``button``.

        The given value is passed to the calculator directly. Valid buttons
        are everything that the calculator accepts.

        Examples:
        | Push Button | 1 |
        | Push Button | C |

        Use `Push Buttons` if you need to input longer expressions.
        """
        self._result = self._calc.push(button)

    def push_buttons(self, buttons):
        """Pushes the specified ``buttons``.

        Uses `Push Button` to push all the buttons that must be given as
        a single string. Possible spaces are ignored.

        Example:
        | Push Buttons | 1 + 2 = |
        """
        for button in buttons.replace(" ", ""):
            self.push_button(button)

    def result_should_be(self, expected):
        """Verifies that the current result is ``expected``.

        Example:
        | Push Buttons     | 1 + 2 = |
        | Result Should Be | 3       |
        """
        if self._result != expected:
            raise AssertionError("%s != %s" % (self._result, expected))

    def should_cause_error(self, expression):
        """Verifies that calculating the given ``expression`` causes an error.

        The error message is returned and can be verified using, for example,
        `Should Be Equal` or other keywords in `BuiltIn` library.

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
            raise AssertionError("'%s' should have caused an error." % expression)


# Robot Framework imports this file by path (`Library  calculator_library.py`),
# which makes it a module library. Expose module-level keywords and ensure state
# is reset between test cases.
try:
    from robot.libraries.BuiltIn import BuiltIn
except Exception:  # pragma: no cover
    BuiltIn = None


ROBOT_LIBRARY_SCOPE = "TEST CASE"
_LIB = None
_CURRENT_TEST = None


def _get_test_name():
    if BuiltIn is None:
        return None
    try:
        return BuiltIn().get_variable_value("${TEST NAME}")
    except Exception:
        return None


def _lib():
    global _LIB, _CURRENT_TEST
    test_name = _get_test_name()
    if _LIB is None or test_name != _CURRENT_TEST:
        _LIB = CalculatorLibrary()
        _CURRENT_TEST = test_name
    return _LIB


def push_button(button):
    _lib().push_button(button)


def push_buttons(buttons):
    _lib().push_buttons(buttons)


def result_should_be(expected):
    _lib().result_should_be(expected)


def should_cause_error(expression):
    return _lib().should_cause_error(expression)
