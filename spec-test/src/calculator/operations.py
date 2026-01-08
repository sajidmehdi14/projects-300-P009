"""Arithmetic operations and domain entities for the calculator.

This module contains the Operator enum and will contain arithmetic
operation functions and the Calculation value object.
"""

from enum import Enum
from calculator.exceptions import InvalidOperatorError


class Operator(Enum):
    """Enumeration of supported arithmetic operators.

    Each operator has a symbol (string representation) and a name.
    The symbol is what the user types, and the name is the operation.

    Attributes:
        ADD: Addition operator (+)
        SUBTRACT: Subtraction operator (-)
        MULTIPLY: Multiplication operator (*)
        DIVIDE: Division operator (/)
    """

    ADD = ("+", "add")
    SUBTRACT = ("-", "subtract")
    MULTIPLY = ("*", "multiply")
    DIVIDE = ("/", "divide")

    @property
    def symbol(self) -> str:
        """Get the string symbol for this operator.

        Returns:
            The operator symbol (e.g., "+", "-", "*", "/")
        """
        return self.value[0]

    @property
    def operation_name(self) -> str:
        """Get the operation name for this operator.

        Returns:
            The operation name (e.g., "add", "subtract", "multiply", "divide")
        """
        return self.value[1]

    @classmethod
    def from_string(cls, symbol: str) -> "Operator":
        """Create an Operator from a string symbol.

        Args:
            symbol: The operator symbol ("+", "-", "*", or "/")

        Returns:
            The corresponding Operator enum value

        Raises:
            InvalidOperatorError: If the symbol is not a supported operator
        """
        for operator in cls:
            if operator.symbol == symbol:
                return operator

        # If we get here, the symbol is not supported
        raise InvalidOperatorError(
            f"Error: Unsupported operator: {symbol}. Use +, -, *, /"
        )
