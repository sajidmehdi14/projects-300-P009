"""Arithmetic operations and domain entities for the calculator.

This module contains the Operator enum and will contain arithmetic
operation functions and the Calculation value object.
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from calculator.exceptions import DivisionByZeroError, InvalidOperatorError


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
        raise InvalidOperatorError(f"Error: Unsupported operator: {symbol}. Use +, -, *, /")


# ============================================================================
# Arithmetic Operation Functions
# ============================================================================


def add(left: Decimal, right: Decimal) -> Decimal:
    """Add two decimal numbers.

    Args:
        left: First operand
        right: Second operand

    Returns:
        Sum of left and right
    """
    return left + right


def subtract(left: Decimal, right: Decimal) -> Decimal:
    """Subtract two decimal numbers.

    Args:
        left: First operand
        right: Second operand

    Returns:
        Difference of left and right (left - right)
    """
    return left - right


def multiply(left: Decimal, right: Decimal) -> Decimal:
    """Multiply two decimal numbers.

    Args:
        left: First operand
        right: Second operand

    Returns:
        Product of left and right
    """
    return left * right


def divide(left: Decimal, right: Decimal) -> Decimal:
    """Divide two decimal numbers.

    Args:
        left: First operand (numerator)
        right: Second operand (denominator)

    Returns:
        Quotient of left divided by right

    Raises:
        DivisionByZeroError: If right is zero
    """
    if right == Decimal("0"):
        raise DivisionByZeroError("Error: Division by zero is not allowed")
    return left / right


# ============================================================================
# Calculation Value Object
# ============================================================================


@dataclass(frozen=True)
class Calculation:
    """Value object representing a single arithmetic calculation.

    This is an immutable object that encapsulates two operands and an operator,
    providing a method to execute the calculation.

    Attributes:
        left_operand: First numeric operand
        operator: Arithmetic operation to perform
        right_operand: Second numeric operand
    """

    left_operand: Decimal
    operator: Operator
    right_operand: Decimal

    def execute(self) -> Decimal:
        """Execute the calculation and return the result.

        Returns:
            The result of applying the operator to the operands

        Raises:
            DivisionByZeroError: If operation is division and right_operand is zero
        """
        if self.operator == Operator.ADD:
            return add(self.left_operand, self.right_operand)
        elif self.operator == Operator.SUBTRACT:
            return subtract(self.left_operand, self.right_operand)
        elif self.operator == Operator.MULTIPLY:
            return multiply(self.left_operand, self.right_operand)
        elif self.operator == Operator.DIVIDE:
            return divide(self.left_operand, self.right_operand)
        else:
            # This should never happen with proper typing, but for completeness
            raise ValueError(f"Unknown operator: {self.operator}")
