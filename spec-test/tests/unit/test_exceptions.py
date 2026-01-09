"""Unit tests for calculator exception classes.

Tests the custom exception hierarchy to ensure proper inheritance
and message handling per specification requirements.
"""

import pytest

from calculator.exceptions import (
    CalculatorError,
    DivisionByZeroError,
    InvalidInputError,
    InvalidOperatorError,
)


class TestCalculatorError:
    """Tests for base CalculatorError exception."""

    def test_calculator_error_is_exception(self) -> None:
        """CalculatorError should inherit from Exception."""
        assert issubclass(CalculatorError, Exception)

    def test_calculator_error_can_be_raised(self) -> None:
        """CalculatorError should be raisable with a message."""
        with pytest.raises(CalculatorError) as exc_info:
            raise CalculatorError("Test error")
        assert str(exc_info.value) == "Test error"


class TestInvalidInputError:
    """Tests for InvalidInputError exception."""

    def test_invalid_input_error_inherits_from_calculator_error(self) -> None:
        """InvalidInputError should inherit from CalculatorError."""
        assert issubclass(InvalidInputError, CalculatorError)

    def test_invalid_input_error_can_be_raised(self) -> None:
        """InvalidInputError should be raisable with a message."""
        with pytest.raises(InvalidInputError) as exc_info:
            raise InvalidInputError("Invalid input")
        assert str(exc_info.value) == "Invalid input"

    def test_invalid_input_error_catchable_as_calculator_error(self) -> None:
        """InvalidInputError should be catchable as CalculatorError."""
        with pytest.raises(CalculatorError):
            raise InvalidInputError("Invalid input")


class TestInvalidOperatorError:
    """Tests for InvalidOperatorError exception."""

    def test_invalid_operator_error_inherits_from_invalid_input_error(self) -> None:
        """InvalidOperatorError should inherit from InvalidInputError."""
        assert issubclass(InvalidOperatorError, InvalidInputError)

    def test_invalid_operator_error_inherits_from_calculator_error(self) -> None:
        """InvalidOperatorError should be catchable as CalculatorError."""
        assert issubclass(InvalidOperatorError, CalculatorError)

    def test_invalid_operator_error_can_be_raised(self) -> None:
        """InvalidOperatorError should be raisable with a message."""
        with pytest.raises(InvalidOperatorError) as exc_info:
            raise InvalidOperatorError("Unsupported operator: %")
        assert "Unsupported operator: %" in str(exc_info.value)

    def test_invalid_operator_error_catchable_as_invalid_input_error(self) -> None:
        """InvalidOperatorError should be catchable as InvalidInputError."""
        with pytest.raises(InvalidInputError):
            raise InvalidOperatorError("Unsupported operator")


class TestDivisionByZeroError:
    """Tests for DivisionByZeroError exception."""

    def test_division_by_zero_error_inherits_from_calculator_error(self) -> None:
        """DivisionByZeroError should inherit from CalculatorError."""
        assert issubclass(DivisionByZeroError, CalculatorError)

    def test_division_by_zero_error_default_message(self) -> None:
        """DivisionByZeroError should have spec-defined default message."""
        with pytest.raises(DivisionByZeroError) as exc_info:
            raise DivisionByZeroError()
        assert str(exc_info.value) == "Error: Division by zero is not allowed"

    def test_division_by_zero_error_custom_message(self) -> None:
        """DivisionByZeroError should accept custom message."""
        custom_msg = "Cannot divide by zero"
        with pytest.raises(DivisionByZeroError) as exc_info:
            raise DivisionByZeroError(custom_msg)
        assert str(exc_info.value) == custom_msg

    def test_division_by_zero_error_catchable_as_calculator_error(self) -> None:
        """DivisionByZeroError should be catchable as CalculatorError."""
        with pytest.raises(CalculatorError):
            raise DivisionByZeroError()


class TestExceptionHierarchy:
    """Tests for overall exception hierarchy structure."""

    def test_all_exceptions_catchable_as_calculator_error(self) -> None:
        """All custom exceptions should be catchable as CalculatorError."""
        exceptions = [
            InvalidInputError("test"),
            InvalidOperatorError("test"),
            DivisionByZeroError(),
        ]

        for exc in exceptions:
            with pytest.raises(CalculatorError):
                raise exc
