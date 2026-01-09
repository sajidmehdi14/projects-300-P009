"""Unit tests for calculator input parsing.

Tests for User Story 1 (US1): Basic input parsing with positive integers
Tests for User Story 2 (US2): Decimal number parsing (added incrementally)
Tests for User Story 3 (US3): Negative number parsing (added incrementally)
"""

from decimal import Decimal

import pytest

from calculator.exceptions import InvalidInputError, InvalidOperatorError
from calculator.operations import Operator
from calculator.parser import CalculatorInput

# ============================================================================
# User Story 1 Tests: Valid Input Parsing with Positive Integers
# ============================================================================


class TestParserValidInput:
    """Test parser with valid 3-argument input (US1)."""

    def test_parse_addition_positive_integers(self) -> None:
        """T017: Parse valid addition with positive integers."""
        result = CalculatorInput.parse(["5", "+", "3"])
        assert result.calculation.left_operand == Decimal("5")
        assert result.calculation.operator == Operator.ADD
        assert result.calculation.right_operand == Decimal("3")

    def test_parse_subtraction_positive_integers(self) -> None:
        """T017: Parse valid subtraction with positive integers."""
        result = CalculatorInput.parse(["10", "-", "4"])
        assert result.calculation.left_operand == Decimal("10")
        assert result.calculation.operator == Operator.SUBTRACT
        assert result.calculation.right_operand == Decimal("4")

    def test_parse_multiplication_positive_integers(self) -> None:
        """T017: Parse valid multiplication with positive integers."""
        result = CalculatorInput.parse(["7", "*", "6"])
        assert result.calculation.left_operand == Decimal("7")
        assert result.calculation.operator == Operator.MULTIPLY
        assert result.calculation.right_operand == Decimal("6")

    def test_parse_division_positive_integers(self) -> None:
        """T017: Parse valid division with positive integers."""
        result = CalculatorInput.parse(["20", "/", "4"])
        assert result.calculation.left_operand == Decimal("20")
        assert result.calculation.operator == Operator.DIVIDE
        assert result.calculation.right_operand == Decimal("4")

    def test_parse_stores_raw_args(self) -> None:
        """T017: Parser stores original raw arguments."""
        args = ["5", "+", "3"]
        result = CalculatorInput.parse(args)
        assert result.raw_args == args


# ============================================================================
# User Story 1 Tests: Invalid Input Parsing
# ============================================================================


class TestParserInvalidInput:
    """Test parser with invalid input (US1)."""

    def test_parse_too_few_arguments(self) -> None:
        """T018: Parser rejects too few arguments."""
        with pytest.raises(InvalidInputError) as exc_info:
            CalculatorInput.parse(["5", "+"])
        assert "Expected" in str(exc_info.value) and "number" in str(exc_info.value)

    def test_parse_too_many_arguments(self) -> None:
        """T018: Parser rejects too many arguments."""
        with pytest.raises(InvalidInputError) as exc_info:
            CalculatorInput.parse(["5", "+", "3", "extra"])
        assert "Expected" in str(exc_info.value) and "number" in str(exc_info.value)

    def test_parse_empty_arguments(self) -> None:
        """T018: Parser rejects empty argument list."""
        with pytest.raises(InvalidInputError) as exc_info:
            CalculatorInput.parse([])
        assert "Expected" in str(exc_info.value) and "number" in str(exc_info.value)

    def test_parse_invalid_operator(self) -> None:
        """T018: Parser rejects invalid operator."""
        with pytest.raises(InvalidOperatorError) as exc_info:
            CalculatorInput.parse(["5", "%", "3"])
        assert "Unsupported operator: %" in str(exc_info.value)
        assert "Use +, -, *, /" in str(exc_info.value)

    def test_parse_invalid_left_operand(self) -> None:
        """T018: Parser rejects invalid left operand."""
        with pytest.raises(InvalidInputError) as exc_info:
            CalculatorInput.parse(["abc", "+", "3"])
        assert "Invalid number: abc" in str(exc_info.value)

    def test_parse_invalid_right_operand(self) -> None:
        """T018: Parser rejects invalid right operand."""
        with pytest.raises(InvalidInputError) as exc_info:
            CalculatorInput.parse(["5", "+", "xyz"])
        assert "Invalid number: xyz" in str(exc_info.value)

    def test_parse_both_operands_invalid(self) -> None:
        """T018: Parser rejects when both operands are invalid."""
        with pytest.raises(InvalidInputError) as exc_info:
            CalculatorInput.parse(["abc", "+", "xyz"])
        # Should catch first invalid operand
        assert "Invalid number" in str(exc_info.value)


# ============================================================================
# User Story 2 Tests: Decimal Number Parsing
# ============================================================================


class TestParserDecimalNumbers:
    """Test parser with decimal number strings (US2)."""

    def test_parse_decimal_operands(self) -> None:
        """T039: Parse decimal number strings."""
        result = CalculatorInput.parse(["3.5", "+", "2.1"])
        assert result.calculation.left_operand == Decimal("3.5")
        assert result.calculation.right_operand == Decimal("2.1")

    def test_parse_mixed_decimal_and_integer(self) -> None:
        """T039: Parse mix of decimal and integer strings."""
        result = CalculatorInput.parse(["10.5", "*", "2"])
        assert result.calculation.left_operand == Decimal("10.5")
        assert result.calculation.right_operand == Decimal("2")

    def test_parse_decimal_with_trailing_zeros(self) -> None:
        """T039: Parse decimal with trailing zeros."""
        result = CalculatorInput.parse(["5.00", "+", "3.50"])
        assert result.calculation.left_operand == Decimal("5.00")
        assert result.calculation.right_operand == Decimal("3.50")

    def test_parse_decimal_point_one_plus_point_two(self) -> None:
        """T039: Parse the classic 0.1 + 0.2 case."""
        result = CalculatorInput.parse(["0.1", "+", "0.2"])
        assert result.calculation.left_operand == Decimal("0.1")
        assert result.calculation.right_operand == Decimal("0.2")

    def test_parse_invalid_decimal_format(self) -> None:
        """T039: Reject malformed decimal strings."""
        with pytest.raises(InvalidInputError) as exc_info:
            CalculatorInput.parse(["3.5.2", "+", "1"])
        assert "Invalid number: 3.5.2" in str(exc_info.value)


# ============================================================================
# User Story 3 Tests: Negative Number Parsing
# ============================================================================


class TestParserNegativeNumbers:
    """Test parser with negative number strings (US3)."""

    def test_parse_negative_left_operand(self) -> None:
        """T049: Parse negative left operand."""
        result = CalculatorInput.parse(["-5", "+", "3"])
        assert result.calculation.left_operand == Decimal("-5")
        assert result.calculation.right_operand == Decimal("3")

    def test_parse_negative_right_operand(self) -> None:
        """T049: Parse negative right operand."""
        result = CalculatorInput.parse(["10", "-", "-4"])
        assert result.calculation.left_operand == Decimal("10")
        assert result.calculation.operator == Operator.SUBTRACT
        assert result.calculation.right_operand == Decimal("-4")

    def test_parse_both_operands_negative(self) -> None:
        """T049: Parse both operands negative."""
        result = CalculatorInput.parse(["-8", "*", "-2"])
        assert result.calculation.left_operand == Decimal("-8")
        assert result.calculation.right_operand == Decimal("-2")

    def test_parse_negative_decimal(self) -> None:
        """T049: Parse negative decimal numbers."""
        result = CalculatorInput.parse(["-3.5", "+", "2.1"])
        assert result.calculation.left_operand == Decimal("-3.5")
        assert result.calculation.right_operand == Decimal("2.1")

    def test_parse_distinguishes_minus_operator_from_negative_sign(self) -> None:
        """T049: Parser correctly distinguishes '-' operator from negative sign."""
        # This is "-5" (negative five) minus "3" (positive three)
        result = CalculatorInput.parse(["-5", "-", "3"])
        assert result.calculation.left_operand == Decimal("-5")
        assert result.calculation.operator == Operator.SUBTRACT
        assert result.calculation.right_operand == Decimal("3")
