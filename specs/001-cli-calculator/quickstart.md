# Quickstart Guide: Basic CLI Calculator

**Feature**: 001-cli-calculator
**Purpose**: End-user guide for using the CLI calculator
**Last Updated**: 2026-01-08

## Installation

### Prerequisites

- Python 3.11 or higher
- UV package manager

### Install UV

If you don't have UV installed:

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv
```

### Install Calculator

```bash
# Clone repository
git clone <repository-url>
cd calculator

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
uv pip install -e .
```

## Basic Usage

The calculator accepts three command-line arguments:

```bash
calculator <number> <operator> <number>
```

**Format**:
- `<number>`: Any numeric value (positive, negative, or decimal)
- `<operator>`: One of `+`, `-`, `*`, `/`
- `<number>`: Any numeric value (positive, negative, or decimal)

**Important**: Use quotes or escape special characters in shell if needed (e.g., `"*"` for multiplication).

## Examples

### Addition

```bash
$ calculator 5 + 3
8

$ calculator 10.5 + 3.2
13.7

$ calculator -5 + 10
5
```

### Subtraction

```bash
$ calculator 10 - 4
6

$ calculator 5 - 8
-3

$ calculator 10 - -4
14
```

### Multiplication

```bash
$ calculator 7 "*" 6
42

$ calculator 3.5 "*" 2
7

$ calculator -3 "*" 5
-15
```

**Note**: The `*` operator must be quoted or escaped in most shells to prevent glob expansion.

### Division

```bash
$ calculator 20 / 4
5

$ calculator 10.5 / 2
5.25

$ calculator -8 / -2
4
```

## Decimal Precision

The calculator maintains high precision for decimal calculations:

```bash
$ calculator 0.1 + 0.2
0.3

$ calculator 10 / 3
3.333333333

$ calculator 22 / 7
3.142857143
```

Trailing zeros are automatically removed:

```bash
$ calculator 5.0 + 0.0
5

$ calculator 3.500 "*" 2
7
```

## Error Handling

### Division by Zero

```bash
$ calculator 10 / 0
Error: Division by zero is not allowed
```

Exit code: 1

### Invalid Operator

```bash
$ calculator 5 % 3
Error: Unsupported operator: %. Use +, -, *, /
```

Exit code: 1

### Invalid Number Format

```bash
$ calculator abc + 5
Error: Invalid number: abc

$ calculator 5 + xyz
Error: Invalid number: xyz
```

Exit code: 1

### Wrong Number of Arguments

```bash
$ calculator 5 +
Error: Invalid input format. Expected: <number> <operator> <number>

$ calculator 5
Error: Invalid input format. Expected: <number> <operator> <number>

$ calculator
Usage: calculator <number> <operator> <number>
Operators: + (add), - (subtract), * (multiply), / (divide)
```

Exit code: 1 (or 0 for usage display)

## Exit Codes

The calculator uses standard Unix exit codes:

- **0**: Success - calculation completed successfully
- **1**: User error - invalid input or division by zero
- **2**: System error - unexpected failure

## Shell Integration

### Using in Scripts

```bash
#!/bin/bash

# Perform calculation and capture result
result=$(calculator 10 + 5)
echo "Result: $result"

# Check exit code
if calculator 10 / 0 2>/dev/null; then
    echo "Success"
else
    echo "Error occurred"
fi
```

### Chaining Operations

The calculator processes one operation at a time. For multiple operations, use shell arithmetic:

```bash
# Calculate (5 + 3) * 2
step1=$(calculator 5 + 3)    # Returns: 8
result=$(calculator "$step1" "*" 2)  # Returns: 16
echo "$result"
```

## Troubleshooting

### Issue: "Command not found"

**Solution**: Ensure virtual environment is activated and package is installed:

```bash
source .venv/bin/activate
uv pip install -e .
```

### Issue: "Operator not recognized" with `*`

**Solution**: Quote the multiplication operator to prevent shell expansion:

```bash
calculator 5 "*" 6   # Correct
calculator 5 \* 6    # Also correct
calculator 5 * 6     # Wrong - shell expands *
```

### Issue: Unexpected decimal results

**Example**:
```bash
$ calculator 10 / 3
3.333333333  # Expected behavior
```

**Explanation**: The calculator uses decimal arithmetic with high precision. Results are displayed with necessary significant figures, trailing zeros removed.

### Issue: "Invalid number" with negative numbers

**Correct usage**:
```bash
calculator -5 + 3      # Correct
calculator "-5" + 3    # Also correct
calculator - 5 + 3     # Wrong - minus is operator, not part of number
```

## Advanced Usage

### Precision Control

The calculator computes with up to 10 decimal places of precision internally. Display automatically adjusts:

```bash
$ calculator 1 / 3
3.333333333      # Shows significant digits

$ calculator 10 / 2
5                # Removes unnecessary decimals
```

### Large Numbers

Standard Python Decimal precision applies (28 significant digits by default):

```bash
$ calculator 999999999 "*" 999999999
999999998000000001

$ calculator 1e10 + 1e10
20000000000
```

### Scientific Notation

Input and output support scientific notation:

```bash
$ calculator 1e6 + 1e6
2000000

$ calculator 1.5e-10 "*" 2
3E-10
```

## Development Usage

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=calculator --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_operations.py
```

### Type Checking

```bash
# Run mypy type checker
mypy src/
```

### Linting and Formatting

```bash
# Run ruff linter
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/
```

## Getting Help

### Usage Information

```bash
calculator
# Displays usage instructions
```

### Documentation

- Full specification: `specs/001-cli-calculator/spec.md`
- Implementation plan: `specs/001-cli-calculator/plan.md`
- Data model: `specs/001-cli-calculator/data-model.md`

### Support

For issues or questions:
1. Check this quickstart guide
2. Review error messages (they explain the problem)
3. Consult the specification documents
4. Check test files for usage examples: `tests/integration/test_cli.py`

## Summary

**Basic Command**:
```bash
calculator <number> <operator> <number>
```

**Operators**: `+`, `-`, `*` (quote it!), `/`

**Features**:
- Supports positive, negative, and decimal numbers
- High precision decimal arithmetic
- Clear error messages
- Standard Unix exit codes
- Fast execution (<1 second)

**Remember**:
- Quote or escape `*` operator: `calculator 5 "*" 6`
- Division by zero returns error (exit code 1)
- Invalid input shows clear error message with expected format
