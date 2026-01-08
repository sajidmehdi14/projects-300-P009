"""Custom exceptions for the calculator application.

This module defines the exception hierarchy for calculator errors,
enabling type-safe error handling throughout the application.
"""


class CalculatorError(Exception):
    """Base exception for all calculator errors.

    All calculator-specific exceptions inherit from this base class,
    allowing for comprehensive error catching when needed.
    """
    pass


class InvalidInputError(CalculatorError):
    """Raised when input format is invalid.

    This exception is raised when:
    - Wrong number of arguments provided
    - Non-numeric operands are provided
    - Input cannot be parsed as expected

    Args:
        message: Description of the validation error
    """
    pass


class InvalidOperatorError(InvalidInputError):
    """Raised when operator is not supported.

    This exception is raised when the operator symbol is not
    one of the four supported operators: +, -, *, /

    Args:
        message: Description of the operator error, typically including
                the invalid operator symbol and list of valid operators
    """
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero.

    Mathematical division by zero is undefined and must be caught
    and handled explicitly per specification requirements.

    Args:
        message: Error message, defaults to spec-defined message
    """

    def __init__(self, message: str = "Error: Division by zero is not allowed") -> None:
        """Initialize DivisionByZeroError with spec-defined default message.

        Args:
            message: Custom error message, defaults to specification requirement
        """
        super().__init__(message)
