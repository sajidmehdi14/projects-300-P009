# Research: Basic CLI Calculator

**Date**: 2026-01-08
**Feature**: 001-cli-calculator
**Purpose**: Research technical decisions and best practices for Python CLI calculator implementation

## Python Version Selection

**Decision**: Python 3.11+

**Rationale**:
- Python 3.11+ provides better performance (10-60% faster than 3.10)
- Improved error messages aid debugging
- Better type hint support for generic types
- Enhanced exception groups for cleaner error handling
- Widely available on modern systems (released October 2022)

**Alternatives Considered**:
- Python 3.10: Still supported but lacks performance improvements
- Python 3.12: Latest but may not be available on all systems yet
- Rejected Python 3.9 and earlier: Approaching end-of-life

## CLI Argument Handling

**Decision**: Use `sys.argv` directly (no argparse/click)

**Rationale**:
- Spec defines exact three-argument format: `<number> <operator> <number>`
- No optional flags, subcommands, or complex parsing needed
- Aligns with Principle IV (Simplicity): stdlib solution sufficient
- Direct argv handling makes validation logic explicit and testable
- Reduces dependency surface area

**Alternatives Considered**:
- argparse: Over-engineered for three fixed positional arguments
- click: External dependency unnecessary for simple fixed-format input
- Rejected: Both add complexity without proportional value

## Numeric Type Handling

**Decision**: Use `Decimal` type from stdlib for all calculations

**Rationale**:
- Spec SC-005 requires "10 decimal places precision"
- Avoids floating-point representation errors (0.1 + 0.2 = 0.30000000000000004)
- Handles negative numbers and decimals natively
- Provides precise decimal arithmetic for financial/measurement use cases
- No external dependencies required

**Alternatives Considered**:
- float: Insufficient precision, floating-point errors violate spec
- fractions.Fraction: Overkill for decimal use cases, less intuitive output
- External library (mpmath): Unnecessary dependency for fixed precision

**Implementation Notes**:
- Parse input strings to Decimal directly
- Handle InvalidOperation exceptions for non-numeric input
- Format output using string conversion with trailing zero removal

## Testing Strategy

**Decision**: pytest with pytest-cov for coverage reporting

**Rationale**:
- pytest is Python industry standard for testing
- Simple parametrize decorator for testing multiple cases
- Clear assertion syntax without boilerplate
- pytest-cov integrates coverage reporting seamlessly
- Supports constitution requirement of 90%+ coverage

**Alternatives Considered**:
- unittest: More verbose, requires boilerplate test classes
- nose: Deprecated in favor of pytest
- Hypothesis: Property-based testing overkill for simple arithmetic

**Test Organization**:
```
tests/
├── unit/           # Pure function tests (operations, parser)
└── integration/    # CLI end-to-end tests via subprocess
```

## Error Handling Architecture

**Decision**: Custom exception hierarchy with base CalculatorError

**Rationale**:
- Spec defines specific error scenarios (division by zero, invalid input)
- Custom exceptions enable precise error messages per spec requirements
- Type-safe error handling through exception hierarchy
- Aligns with Principle VI (Clear Error Handling)

**Exception Design**:
```python
class CalculatorError(Exception): pass
class DivisionByZeroError(CalculatorError): pass
class InvalidInputError(CalculatorError): pass
class InvalidOperatorError(InvalidInputError): pass
```

**Alternatives Considered**:
- Using built-in exceptions (ValueError, ZeroDivisionError): Less semantic, harder to distinguish calculator errors from other errors
- Single generic exception: Loses type specificity for error handling

## Exit Code Strategy

**Decision**: Standard Unix exit codes

**Rationale**:
- 0: Success (valid calculation completed)
- 1: User error (invalid input, division by zero)
- 2: System error (unexpected failures)
- Enables shell scripting and automation
- Follows Unix conventions per spec FR-011

## Decimal Formatting

**Decision**: Remove trailing zeros, preserve significant digits

**Rationale**:
- Spec states "up to 10 significant figures, trailing zeros removed"
- User expectations: "5.0" → "5", "3.14000" → "3.14"
- Maintains precision for actual decimals: "0.1 + 0.2" → "0.3"
- Python Decimal.normalize() handles this cleanly

**Implementation**:
```python
result = calculation_result.normalize()  # Removes trailing zeros
print(str(result))  # Clean string representation
```

## Project Setup with UV

**Decision**: UV for virtual environment and dependency management

**Rationale**:
- Constitution Principle II mandates UV
- Faster than pip (Rust-based resolver)
- Reproducible builds via lock files
- Simple workflow: `uv venv`, `uv pip install`, `uv sync`

**Dependencies**:
```toml
[project]
dependencies = []  # No runtime dependencies

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
]
```

## Type Checking Configuration

**Decision**: mypy strict mode with no compromises

**Rationale**:
- Constitution Principle I mandates type hints
- Strict mode catches maximum errors at static analysis time
- Small codebase makes strict typing achievable
- No gradual typing needed (greenfield project)

**mypy.ini**:
```ini
[mypy]
python_version = 3.11
strict = True
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

## Linting and Formatting

**Decision**: ruff for both linting and formatting

**Rationale**:
- Single tool for linting + formatting (replaces black, flake8, isort)
- 10-100x faster than alternatives (Rust-based)
- Drop-in replacement for existing Python tools
- Constitution mandates ruff in Code Quality Standards

**Configuration**:
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]  # Standard rules
```

## Package Structure

**Decision**: src-layout with calculator package

**Rationale**:
- Prevents accidental imports of uninstalled package
- Clear separation of source and tests
- Enables `python -m calculator` invocation
- Industry best practice for Python packaging

**Entry Points**:
```python
# src/calculator/__main__.py
if __name__ == "__main__":
    from calculator.cli import main
    sys.exit(main())
```

## Summary of Technical Stack

| Component | Choice | Justification |
|-----------|--------|---------------|
| Language | Python 3.11+ | Performance, type hints, modern features |
| Numeric Type | Decimal | Precision requirements, avoid float errors |
| CLI Parsing | sys.argv | Simplicity, no complex parsing needed |
| Testing | pytest + pytest-cov | Industry standard, good coverage tools |
| Type Checking | mypy strict | Constitution mandate, catch errors early |
| Linting | ruff | Fast, comprehensive, constitution mandate |
| Dependencies | UV | Constitution mandate, fast, reproducible |
| Error Handling | Custom exceptions | Clear semantics, spec requirements |

All technical decisions align with constitution principles (type safety, simplicity, testability, UV, clear errors).
