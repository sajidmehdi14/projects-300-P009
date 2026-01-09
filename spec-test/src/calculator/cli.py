"""Command-line interface for the calculator.

This module provides the main entry point for the calculator CLI,
handling argument parsing, execution, error handling, and output formatting.
"""

import sys

from calculator.exceptions import CalculatorError
from calculator.parser import CalculatorInput


def format_result(result) -> str:  # type: ignore
    """Format a Decimal result for display.

    Removes trailing zeros and unnecessary decimal points.

    Args:
        result: Decimal result to format

    Returns:
        Formatted string representation of the result
    """
    # Normalize removes trailing zeros from decimals
    normalized = result.normalize()
    # Convert to string, avoiding scientific notation
    result_str = str(normalized)

    # If scientific notation is used, convert back to regular notation
    if "E" in result_str or "e" in result_str:
        # Use format with 'f' to avoid scientific notation
        formatted = format(normalized, "f")
        # Only strip trailing zeros after the decimal point
        if "." in formatted:
            formatted = formatted.rstrip("0").rstrip(".")
        return formatted

    return result_str


def display_usage() -> None:
    """Display usage information to stdout."""
    print("Usage: calculator <number> <operator> <number>")
    print("Operators: + (add), - (subtract), * (multiply), / (divide)")


def main() -> int:
    """Main entry point for the calculator CLI.

    Parses command-line arguments, executes the calculation, and displays results.

    Returns:
        Exit code: 0 for success, 1 for user error, 2 for system error
    """
    # Get arguments (excluding program name)
    args = sys.argv[1:]

    # Display usage if no arguments provided
    if len(args) == 0:
        display_usage()
        return 0

    try:
        # Parse input
        calculator_input = CalculatorInput.parse(args)

        # Execute calculation
        result = calculator_input.calculation.execute()

        # Format and display result
        formatted_result = format_result(result)
        print(formatted_result)

        return 0

    except CalculatorError as e:
        # User errors (invalid input, division by zero, etc.)
        print(str(e), file=sys.stderr)
        return 1

    except Exception as e:
        # Unexpected system errors
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        return 2
