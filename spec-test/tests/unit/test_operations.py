"""Unit tests for calculator operations and Calculation value object.

Tests for User Story 1 (US1): Basic Arithmetic with Positive Integers
Tests for User Story 2 (US2): Decimal Number Support (added incrementally)
Tests for User Story 3 (US3): Negative Number Handling (added incrementally)
"""

from decimal import Decimal

import pytest

from calculator.exceptions import DivisionByZeroError
from calculator.operations import Calculation, Operator, add, divide, multiply, subtract

# ============================================================================
# User Story 1 Tests: Basic Operations with Positive Integers
# ============================================================================


class TestAddFunction:
    """Test add function with positive integers (US1)."""

    def test_add_two_positive_integers(self) -> None:
        """T012: Add two positive integers."""
        assert add(Decimal("5"), Decimal("3")) == Decimal("8")

    def test_add_positive_integers_large(self) -> None:
        """T012: Add large positive integers."""
        assert add(Decimal("1000"), Decimal("500")) == Decimal("1500")

    def test_add_zero_to_positive(self) -> None:
        """T012: Add zero to positive integer."""
        assert add(Decimal("10"), Decimal("0")) == Decimal("10")

    def test_add_positive_to_zero(self) -> None:
        """T012: Add positive integer to zero."""
        assert add(Decimal("0"), Decimal("7")) == Decimal("7")


class TestSubtractFunction:
    """Test subtract function with positive integers (US1)."""

    def test_subtract_two_positive_integers(self) -> None:
        """T013: Subtract two positive integers."""
        assert subtract(Decimal("10"), Decimal("4")) == Decimal("6")

    def test_subtract_larger_from_smaller_positive(self) -> None:
        """T013: Subtract larger from smaller (result negative)."""
        assert subtract(Decimal("5"), Decimal("8")) == Decimal("-3")

    def test_subtract_zero_from_positive(self) -> None:
        """T013: Subtract zero from positive."""
        assert subtract(Decimal("10"), Decimal("0")) == Decimal("10")

    def test_subtract_positive_from_zero(self) -> None:
        """T013: Subtract positive from zero."""
        assert subtract(Decimal("0"), Decimal("5")) == Decimal("-5")


class TestMultiplyFunction:
    """Test multiply function with positive integers (US1)."""

    def test_multiply_two_positive_integers(self) -> None:
        """T014: Multiply two positive integers."""
        assert multiply(Decimal("7"), Decimal("6")) == Decimal("42")

    def test_multiply_by_zero(self) -> None:
        """T014: Multiply by zero."""
        assert multiply(Decimal("10"), Decimal("0")) == Decimal("0")

    def test_multiply_by_one(self) -> None:
        """T014: Multiply by one."""
        assert multiply(Decimal("15"), Decimal("1")) == Decimal("15")

    def test_multiply_large_numbers(self) -> None:
        """T014: Multiply large positive integers."""
        assert multiply(Decimal("100"), Decimal("50")) == Decimal("5000")


class TestDivideFunction:
    """Test divide function with positive integers (US1)."""

    def test_divide_two_positive_integers(self) -> None:
        """T015: Divide two positive integers."""
        assert divide(Decimal("20"), Decimal("4")) == Decimal("5")

    def test_divide_with_remainder(self) -> None:
        """T015: Divide with decimal result."""
        result = divide(Decimal("10"), Decimal("3"))
        assert str(result).startswith("3.333333333")

    def test_divide_by_one(self) -> None:
        """T015: Divide by one."""
        assert divide(Decimal("42"), Decimal("1")) == Decimal("42")

    def test_divide_zero_by_positive(self) -> None:
        """T015: Divide zero by positive integer."""
        assert divide(Decimal("0"), Decimal("10")) == Decimal("0")

    def test_divide_by_zero_raises_error(self) -> None:
        """T016: Division by zero raises DivisionByZeroError."""
        with pytest.raises(DivisionByZeroError) as exc_info:
            divide(Decimal("10"), Decimal("0"))
        assert "Division by zero is not allowed" in str(exc_info.value)


# ============================================================================
# User Story 1: Calculation Value Object Tests
# ============================================================================


class TestCalculationWithPositiveIntegers:
    """Test Calculation value object with positive integers (US1)."""

    def test_calculation_addition(self) -> None:
        """Calculation.execute() performs addition correctly."""
        calc = Calculation(Decimal("5"), Operator.ADD, Decimal("3"))
        assert calc.execute() == Decimal("8")

    def test_calculation_subtraction(self) -> None:
        """Calculation.execute() performs subtraction correctly."""
        calc = Calculation(Decimal("10"), Operator.SUBTRACT, Decimal("4"))
        assert calc.execute() == Decimal("6")

    def test_calculation_multiplication(self) -> None:
        """Calculation.execute() performs multiplication correctly."""
        calc = Calculation(Decimal("7"), Operator.MULTIPLY, Decimal("6"))
        assert calc.execute() == Decimal("42")

    def test_calculation_division(self) -> None:
        """Calculation.execute() performs division correctly."""
        calc = Calculation(Decimal("20"), Operator.DIVIDE, Decimal("4"))
        assert calc.execute() == Decimal("5")

    def test_calculation_division_by_zero(self) -> None:
        """Calculation.execute() raises error on division by zero."""
        calc = Calculation(Decimal("10"), Operator.DIVIDE, Decimal("0"))
        with pytest.raises(DivisionByZeroError):
            calc.execute()

    def test_calculation_is_immutable(self) -> None:
        """Calculation is a frozen dataclass (immutable)."""
        calc = Calculation(Decimal("5"), Operator.ADD, Decimal("3"))
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            calc.left_operand = Decimal("10")  # type: ignore


# ============================================================================
# User Story 2 Tests: Decimal Number Support
# ============================================================================


class TestOperationsWithDecimals:
    """Test operations with decimal numbers (US2)."""

    def test_add_decimals(self) -> None:
        """T037: Add two decimal numbers."""
        assert add(Decimal("3.5"), Decimal("2.1")) == Decimal("5.6")

    def test_subtract_decimals(self) -> None:
        """T037: Subtract decimal numbers."""
        assert subtract(Decimal("10.5"), Decimal("3.2")) == Decimal("7.3")

    def test_multiply_decimals(self) -> None:
        """T037: Multiply decimal numbers."""
        assert multiply(Decimal("3.5"), Decimal("2")) == Decimal("7")

    def test_divide_decimals(self) -> None:
        """T037: Divide decimal numbers."""
        assert divide(Decimal("10.5"), Decimal("2")) == Decimal("5.25")

    def test_decimal_precision_point_one_plus_point_two(self) -> None:
        """T038: Decimal precision - 0.1 + 0.2 should equal 0.3 exactly."""
        result = add(Decimal("0.1"), Decimal("0.2"))
        assert result == Decimal("0.3")

    def test_decimal_precision_complex_calculation(self) -> None:
        """T038: Decimal precision maintained in complex calculations."""
        result = multiply(Decimal("0.1"), Decimal("3"))
        assert result == Decimal("0.3")


# ============================================================================
# User Story 3 Tests: Negative Number Support
# ============================================================================


class TestOperationsWithNegatives:
    """Test operations with negative numbers (US3)."""

    def test_add_negative_operands(self) -> None:
        """T047: Add with negative operands."""
        assert add(Decimal("-5"), Decimal("3")) == Decimal("-2")
        assert add(Decimal("5"), Decimal("-3")) == Decimal("2")
        assert add(Decimal("-5"), Decimal("-3")) == Decimal("-8")

    def test_subtract_negative_operands(self) -> None:
        """T047: Subtract with negative operands."""
        assert subtract(Decimal("-5"), Decimal("3")) == Decimal("-8")
        assert subtract(Decimal("5"), Decimal("-3")) == Decimal("8")
        assert subtract(Decimal("-5"), Decimal("-3")) == Decimal("-2")

    def test_multiply_negative_operands(self) -> None:
        """T047: Multiply with negative operands."""
        assert multiply(Decimal("-3"), Decimal("5")) == Decimal("-15")
        assert multiply(Decimal("3"), Decimal("-5")) == Decimal("-15")
        assert multiply(Decimal("-3"), Decimal("-5")) == Decimal("15")

    def test_divide_negative_operands(self) -> None:
        """T047: Divide with negative operands."""
        assert divide(Decimal("-8"), Decimal("2")) == Decimal("-4")
        assert divide(Decimal("8"), Decimal("-2")) == Decimal("-4")
        assert divide(Decimal("-8"), Decimal("-2")) == Decimal("4")

    def test_negative_result_cases(self) -> None:
        """T048: Test cases that produce negative results."""
        assert subtract(Decimal("3"), Decimal("10")) == Decimal("-7")
        assert multiply(Decimal("-2"), Decimal("4")) == Decimal("-8")
        assert divide(Decimal("-20"), Decimal("5")) == Decimal("-4")
