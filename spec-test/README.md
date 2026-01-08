# Calculator - Basic CLI Calculator

A simple command-line calculator for basic arithmetic operations.

## Features

- **Four Basic Operations**: Addition (+), Subtraction (-), Multiplication (*), Division (/)
- **Number Support**: Positive integers, decimal numbers, and negative numbers
- **Error Handling**: Clear error messages for invalid input and division by zero
- **High Precision**: Decimal arithmetic with up to 10 decimal places
- **Type-Safe**: Full type hints with mypy strict mode validation

## Requirements

- Python 3.11 or higher
- UV package manager

## Installation

### Install UV

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv
```

### Install Calculator

```bash
# Clone the repository
git clone <repository-url>
cd calculator

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
```

## Usage

The calculator accepts three command-line arguments:

```bash
calculator <number> <operator> <number>
```

### Examples

**Addition:**
```bash
calculator 5 + 3
# Output: 8
```

**Subtraction:**
```bash
calculator 10 - 4
# Output: 6
```

**Multiplication:**
```bash
calculator 7 "*" 6
# Output: 42

# Note: Quote the * operator to prevent shell expansion
```

**Division:**
```bash
calculator 20 / 4
# Output: 5
```

**Decimal Numbers:**
```bash
calculator 3.5 + 2.1
# Output: 5.6

calculator 10 / 3
# Output: 3.333333333
```

**Negative Numbers:**
```bash
calculator -5 + 3
# Output: -2

calculator 10 - -4
# Output: 14
```

### Error Handling

**Division by zero:**
```bash
calculator 10 / 0
# Output: Error: Division by zero is not allowed
# Exit code: 1
```

**Invalid input:**
```bash
calculator abc + 5
# Output: Error: Invalid number: abc
# Exit code: 1
```

## Development

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
mypy src/
```

### Linting and Formatting

```bash
# Check code
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/
```

## Architecture

The calculator follows a clean, modular architecture:

- **src/calculator/operations.py**: Pure arithmetic functions and Calculation value object
- **src/calculator/parser.py**: Input parsing and validation
- **src/calculator/exceptions.py**: Custom exception hierarchy
- **src/calculator/cli.py**: CLI entry point and error handling

All code follows:
- Type safety with mypy strict mode
- Test-first development (TDD)
- Pure functions for testability
- Clear error messages

## Exit Codes

- **0**: Success - calculation completed
- **1**: User error - invalid input or division by zero
- **2**: System error - unexpected failure

## License

MIT License

## Documentation

For more detailed documentation, see:
- [Feature Specification](./specs/001-cli-calculator/spec.md)
- [Implementation Plan](./specs/001-cli-calculator/plan.md)
- [Quickstart Guide](./specs/001-cli-calculator/quickstart.md)
