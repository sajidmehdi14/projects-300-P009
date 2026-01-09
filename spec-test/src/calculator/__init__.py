"""Calculator package for basic arithmetic operations.

This package provides a command-line calculator with support for:
- Four basic operations: addition, subtraction, multiplication, division
- Positive integers, decimal numbers, and negative numbers
- Clear error messages and proper exit codes
- Type-safe implementation with mypy strict mode
"""

from calculator.exceptions import (
    CalculatorError,
    DivisionByZeroError,
    InvalidInputError,
    InvalidOperatorError,
)
from calculator.operations import Operator

__version__ = "0.1.0"

__all__ = [
    "CalculatorError",
    "InvalidInputError",
    "InvalidOperatorError",
    "DivisionByZeroError",
    "Operator",
]
