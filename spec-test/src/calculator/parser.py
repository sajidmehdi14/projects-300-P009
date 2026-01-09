"""Input parsing for the calculator.

This module handles parsing command-line arguments into validated Calculation objects.
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from calculator.exceptions import InvalidInputError
from calculator.operations import Calculation, Operator


@dataclass(frozen=True)
class CalculatorInput:
    """Value object representing parsed and validated command-line input.

    This immutable object stores both the raw command-line arguments and the
    parsed Calculation object.

    Attributes:
        raw_args: Original command-line arguments
        calculation: Parsed and validated Calculation object
    """

    raw_args: list[str]
    calculation: Calculation

    @classmethod
    def parse(cls, args: list[str]) -> "CalculatorInput":
        """Parse command-line arguments into a CalculatorInput.

        Args:
            args: List of command-line arguments (excluding program name)
                  Expected format: [number, operator, number]

        Returns:
            Parsed CalculatorInput object

        Raises:
            InvalidInputError: If argument format is invalid or numbers are malformed
            InvalidOperatorError: If operator is not supported
        """
        # Validate argument count
        if len(args) != 3:
            raise InvalidInputError(
                "Error: Invalid input format. Expected: <number> <operator> <number>"
            )

        left_str, operator_str, right_str = args

        # Parse left operand
        try:
            left_operand = Decimal(left_str)
        except (InvalidOperation, ValueError):
            raise InvalidInputError(f"Error: Invalid number: {left_str}")

        # Parse operator
        operator = Operator.from_string(operator_str)

        # Parse right operand
        try:
            right_operand = Decimal(right_str)
        except (InvalidOperation, ValueError):
            raise InvalidInputError(f"Error: Invalid number: {right_str}")

        # Create Calculation object
        calculation = Calculation(left_operand, operator, right_operand)

        return cls(raw_args=args, calculation=calculation)
