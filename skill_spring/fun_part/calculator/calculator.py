class Calculator:
    BUTTONS = "1234567890+-*/C="

    def __init__(self):
        self._expression = ""

    def push_single_button(self, button):
        if button not in self.BUTTONS:
            raise CalculationError("Invalid button '%s'." % button)
        if button == "=":
            self._expression = self._calculate_expression(self._expression)
        elif button == "C":
            self._expression = ""
        elif button == "/":
            self._expression += "//"  # Integer division also in Python 3
        else:
            self._expression += button
        return self._expression

    def _calculate_expression(self, expression):
        try:
            return str(eval(expression))
        except SyntaxError:
            raise CalculationError("Invalid expression.")
        except ZeroDivisionError:
            raise CalculationError("Division by zero.")


class CalculationError(Exception):
    pass
