"""Integration tests for CLI calculator end-to-end functionality.

Tests for User Story 1 (US1): Basic arithmetic with positive integers
Tests for User Story 2 (US2): Decimal number support (added incrementally)
Tests for User Story 3 (US3): Negative number handling (added incrementally)
"""

import subprocess
import sys
from pathlib import Path

# ============================================================================
# Helper Functions
# ============================================================================


def run_calculator(*args: str) -> tuple[int, str, str]:
    """Run the calculator CLI with given arguments.

    Args:
        *args: Command-line arguments to pass to calculator

    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    # Use python -m calculator to run the CLI
    cmd = [sys.executable, "-m", "calculator", *args]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent.parent,  # Project root
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


# ============================================================================
# User Story 1 Tests: Basic Arithmetic with Positive Integers
# ============================================================================


class TestCLIAddition:
    """Test CLI addition with positive integers (US1)."""

    def test_cli_add_positive_integers(self) -> None:
        """T019: CLI addition with positive integers."""
        exit_code, stdout, stderr = run_calculator("5", "+", "3")
        assert exit_code == 0
        assert stdout == "8"
        assert stderr == ""

    def test_cli_add_large_numbers(self) -> None:
        """T019: CLI addition with large positive integers."""
        exit_code, stdout, stderr = run_calculator("1000", "+", "500")
        assert exit_code == 0
        assert stdout == "1500"
        assert stderr == ""


class TestCLISubtraction:
    """Test CLI subtraction with positive integers (US1)."""

    def test_cli_subtract_positive_integers(self) -> None:
        """T019: CLI subtraction with positive integers."""
        exit_code, stdout, stderr = run_calculator("10", "-", "4")
        assert exit_code == 0
        assert stdout == "6"
        assert stderr == ""

    def test_cli_subtract_result_negative(self) -> None:
        """T019: CLI subtraction resulting in negative."""
        exit_code, stdout, stderr = run_calculator("5", "-", "8")
        assert exit_code == 0
        assert stdout == "-3"
        assert stderr == ""


class TestCLIMultiplication:
    """Test CLI multiplication with positive integers (US1)."""

    def test_cli_multiply_positive_integers(self) -> None:
        """T019: CLI multiplication with positive integers."""
        exit_code, stdout, stderr = run_calculator("7", "*", "6")
        assert exit_code == 0
        assert stdout == "42"
        assert stderr == ""

    def test_cli_multiply_by_zero(self) -> None:
        """T019: CLI multiplication by zero."""
        exit_code, stdout, stderr = run_calculator("10", "*", "0")
        assert exit_code == 0
        assert stdout == "0"
        assert stderr == ""


class TestCLIDivision:
    """Test CLI division with positive integers (US1)."""

    def test_cli_divide_positive_integers(self) -> None:
        """T019: CLI division with positive integers."""
        exit_code, stdout, stderr = run_calculator("20", "/", "4")
        assert exit_code == 0
        assert stdout == "5"
        assert stderr == ""

    def test_cli_divide_with_decimal_result(self) -> None:
        """T019: CLI division with decimal result."""
        exit_code, stdout, stderr = run_calculator("10", "/", "3")
        assert exit_code == 0
        assert stdout.startswith("3.333333333")
        assert stderr == ""

    def test_cli_divide_by_zero_error(self) -> None:
        """T019: CLI division by zero returns error."""
        exit_code, stdout, stderr = run_calculator("10", "/", "0")
        assert exit_code == 1
        assert stdout == ""
        assert "Error: Division by zero is not allowed" in stderr


# ============================================================================
# User Story 1 Tests: Error Handling
# ============================================================================


class TestCLIErrorHandling:
    """Test CLI error handling (US1)."""

    def test_cli_invalid_operator(self) -> None:
        """T019: CLI rejects invalid operator."""
        exit_code, stdout, stderr = run_calculator("5", "%", "3")
        assert exit_code == 1
        assert stdout == ""
        assert "Error: Unsupported operator: %" in stderr
        assert "Use +, -, *, /" in stderr

    def test_cli_invalid_left_operand(self) -> None:
        """T019: CLI rejects invalid left operand."""
        exit_code, stdout, stderr = run_calculator("abc", "+", "3")
        assert exit_code == 1
        assert stdout == ""
        assert "Error: Invalid number: abc" in stderr

    def test_cli_invalid_right_operand(self) -> None:
        """T019: CLI rejects invalid right operand."""
        exit_code, stdout, stderr = run_calculator("5", "+", "xyz")
        assert exit_code == 1
        assert stdout == ""
        assert "Error: Invalid number: xyz" in stderr

    def test_cli_too_few_arguments(self) -> None:
        """T019: CLI rejects too few arguments."""
        exit_code, stdout, stderr = run_calculator("5", "+")
        assert exit_code == 1
        assert stdout == ""
        assert "Error: Invalid input format" in stderr
        assert "Expected: <number> <operator> <number>" in stderr

    def test_cli_too_many_arguments(self) -> None:
        """T019: CLI rejects too many arguments."""
        exit_code, stdout, stderr = run_calculator("5", "+", "3", "extra")
        assert exit_code == 1
        assert stdout == ""
        assert "Error: Invalid input format" in stderr

    def test_cli_no_arguments_shows_usage(self) -> None:
        """T019: CLI with no arguments shows usage message."""
        exit_code, stdout, stderr = run_calculator()
        assert exit_code == 0  # Usage display is not an error
        assert "Usage: calculator <number> <operator> <number>" in stdout
        assert "Operators:" in stdout
        assert stderr == ""


# ============================================================================
# User Story 2 Tests: Decimal Number Support
# ============================================================================


class TestCLIDecimalNumbers:
    """Test CLI with decimal numbers (US2)."""

    def test_cli_add_decimals(self) -> None:
        """T040: CLI addition with decimal numbers."""
        exit_code, stdout, stderr = run_calculator("3.5", "+", "2.1")
        assert exit_code == 0
        assert stdout == "5.6"
        assert stderr == ""

    def test_cli_divide_decimals(self) -> None:
        """T040: CLI division with decimal numbers."""
        exit_code, stdout, stderr = run_calculator("10.5", "/", "2")
        assert exit_code == 0
        assert stdout == "5.25"
        assert stderr == ""

    def test_cli_decimal_precision_point_one_plus_point_two(self) -> None:
        """T040: CLI correctly handles 0.1 + 0.2 = 0.3."""
        exit_code, stdout, stderr = run_calculator("0.1", "+", "0.2")
        assert exit_code == 0
        assert stdout == "0.3"
        assert stderr == ""

    def test_cli_removes_trailing_zeros(self) -> None:
        """T040: CLI removes trailing zeros from decimal results."""
        exit_code, stdout, stderr = run_calculator("5.0", "+", "0.0")
        assert exit_code == 0
        assert stdout == "5"
        assert stderr == ""

    def test_cli_multiply_decimal_result_no_trailing_zeros(self) -> None:
        """T040: CLI multiplication removes trailing zeros."""
        exit_code, stdout, stderr = run_calculator("3.5", "*", "2")
        assert exit_code == 0
        assert stdout == "7"
        assert stderr == ""


# ============================================================================
# User Story 3 Tests: Negative Number Handling
# ============================================================================


class TestCLINegativeNumbers:
    """Test CLI with negative numbers (US3)."""

    def test_cli_add_negative_and_positive(self) -> None:
        """T050: CLI addition with negative and positive numbers."""
        exit_code, stdout, stderr = run_calculator("-5", "+", "3")
        assert exit_code == 0
        assert stdout == "-2"
        assert stderr == ""

    def test_cli_subtract_negative_from_positive(self) -> None:
        """T050: CLI subtraction with negative operand (double negative)."""
        exit_code, stdout, stderr = run_calculator("10", "-", "-4")
        assert exit_code == 0
        assert stdout == "14"
        assert stderr == ""

    def test_cli_multiply_negatives(self) -> None:
        """T050: CLI multiplication with negative operands."""
        exit_code, stdout, stderr = run_calculator("-3", "*", "5")
        assert exit_code == 0
        assert stdout == "-15"
        assert stderr == ""

        exit_code, stdout, stderr = run_calculator("-3", "*", "-5")
        assert exit_code == 0
        assert stdout == "15"
        assert stderr == ""

    def test_cli_divide_negatives(self) -> None:
        """T050: CLI division with negative operands."""
        exit_code, stdout, stderr = run_calculator("-8", "/", "2")
        assert exit_code == 0
        assert stdout == "-4"
        assert stderr == ""

        exit_code, stdout, stderr = run_calculator("-8", "/", "-2")
        assert exit_code == 0
        assert stdout == "4"
        assert stderr == ""

    def test_cli_negative_decimal_numbers(self) -> None:
        """T050: CLI with negative decimal numbers."""
        exit_code, stdout, stderr = run_calculator("-3.5", "+", "2.1")
        assert exit_code == 0
        assert stdout == "-1.4"
        assert stderr == ""
