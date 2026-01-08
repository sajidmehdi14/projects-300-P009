# Data Model: Basic CLI Calculator

**Date**: 2026-01-08
**Feature**: 001-cli-calculator
**Purpose**: Define domain entities and their relationships for the calculator

## Overview

The calculator is a stateless system with no persistent data. The domain model consists of value objects representing calculations and operations. All entities are immutable and have no lifecycle beyond a single calculation.

## Domain Entities

### Operator (Enum)

Represents the four supported arithmetic operations.

**Type**: Value Object (Enum)

**Values**:
- `ADD`: Addition operator (+)
- `SUBTRACT`: Subtraction operator (-)
- `MULTIPLY`: Multiplication operator (*)
- `DIVIDE`: Division operator (/)

**Validation Rules**:
- Must be one of the four defined operators
- Invalid operators raise `InvalidOperatorError`

**String Representation**:
```python
Operator.ADD.symbol      # "+"
Operator.SUBTRACT.symbol # "-"
Operator.MULTIPLY.symbol # "*"
Operator.DIVIDE.symbol   # "/"
```

**Type Signature**:
```python
from enum import Enum
from typing import Literal

class Operator(Enum):
    ADD: tuple[str, str] = ("+", "add")
    SUBTRACT: tuple[str, str] = ("-", "subtract")
    MULTIPLY: tuple[str, str] = ("*", "multiply")
    DIVIDE: tuple[str, str] = ("/", "divide")

    @property
    def symbol(self) -> str: ...

    @classmethod
    def from_string(cls, symbol: str) -> "Operator": ...
```

---

### Calculation (Value Object)

Represents a single arithmetic calculation with two operands and one operator.

**Type**: Value Object (Immutable)

**Attributes**:
- `left_operand: Decimal` - First numeric operand (can be positive, negative, or decimal)
- `operator: Operator` - Arithmetic operation to perform
- `right_operand: Decimal` - Second numeric operand (can be positive, negative, or decimal)

**Validation Rules**:
- `left_operand`: Must be a valid Decimal value
- `operator`: Must be a valid Operator enum value
- `right_operand`: Must be a valid Decimal value
- Special case: If `operator == Operator.DIVIDE` and `right_operand == 0`, raise `DivisionByZeroError`

**Operations**:
- `execute() -> Decimal`: Performs the calculation and returns the result

**Invariants**:
- All fields are immutable after construction
- Division by zero is detected at execution time
- No arithmetic overflow (Decimal handles arbitrary precision)

**Type Signature**:
```python
from decimal import Decimal
from dataclasses import dataclass

@dataclass(frozen=True)
class Calculation:
    left_operand: Decimal
    operator: Operator
    right_operand: Decimal

    def execute(self) -> Decimal:
        """Execute the calculation and return the result.

        Raises:
            DivisionByZeroError: If dividing by zero
        """
        ...
```

**Example Instances**:
```python
# Addition
Calculation(Decimal("5"), Operator.ADD, Decimal("3"))  # Result: 8

# Subtraction with negatives
Calculation(Decimal("-5"), Operator.SUBTRACT, Decimal("3"))  # Result: -8

# Multiplication with decimals
Calculation(Decimal("3.5"), Operator.MULTIPLY, Decimal("2"))  # Result: 7.0

# Division
Calculation(Decimal("10"), Operator.DIVIDE, Decimal("2"))  # Result: 5

# Division by zero (error case)
Calculation(Decimal("10"), Operator.DIVIDE, Decimal("0"))  # Raises DivisionByZeroError
```

---

### CalculatorInput (Value Object)

Represents parsed and validated command-line input.

**Type**: Value Object (Immutable)

**Attributes**:
- `raw_args: list[str]` - Original command-line arguments
- `calculation: Calculation` - Parsed calculation object

**Validation Rules**:
- `raw_args`: Must contain exactly 3 elements
- First element: Must be parseable as Decimal
- Second element: Must be valid operator symbol
- Third element: Must be parseable as Decimal

**Parsing Errors**:
- Too few/many arguments → `InvalidInputError("Expected 3 arguments: <number> <operator> <number>")`
- Non-numeric operands → `InvalidInputError("Invalid number: {value}")`
- Invalid operator → `InvalidOperatorError("Unsupported operator: {symbol}. Use +, -, *, /")`

**Type Signature**:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CalculatorInput:
    raw_args: list[str]
    calculation: Calculation

    @classmethod
    def parse(cls, args: list[str]) -> "CalculatorInput":
        """Parse command-line arguments into a CalculatorInput.

        Args:
            args: List of command-line arguments (excluding program name)

        Returns:
            Parsed CalculatorInput object

        Raises:
            InvalidInputError: If argument format is invalid
            InvalidOperatorError: If operator is not supported
        """
        ...
```

---

## Exception Hierarchy

Custom exceptions for domain-specific error handling.

```python
class CalculatorError(Exception):
    """Base exception for all calculator errors."""
    pass

class InvalidInputError(CalculatorError):
    """Raised when input format is invalid."""
    pass

class InvalidOperatorError(InvalidInputError):
    """Raised when operator is not supported."""
    pass

class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass
```

**Error Messages** (per spec requirements):
- Division by zero: `"Error: Division by zero is not allowed"`
- Invalid input: `"Error: Invalid input format. Expected: <number> <operator> <number>"`
- Invalid operator: `"Error: Unsupported operator: {symbol}. Use +, -, *, /"`
- Invalid number: `"Error: Invalid number: {value}"`

---

## Data Flow

```
1. CLI Entry Point
   ↓
2. Parse sys.argv → CalculatorInput
   ↓ (raises InvalidInputError/InvalidOperatorError if invalid)
3. Extract Calculation from CalculatorInput
   ↓
4. Execute Calculation → Decimal result
   ↓ (raises DivisionByZeroError if dividing by zero)
5. Format result (normalize, remove trailing zeros)
   ↓
6. Print to stdout, exit 0
```

**Error Flow**:
```
Exception Raised
   ↓
Catch in main()
   ↓
Print error message to stderr
   ↓
Exit with code 1 (user error)
```

---

## Relationships

```
CalculatorInput
    ├── raw_args: list[str]
    └── calculation: Calculation
            ├── left_operand: Decimal
            ├── operator: Operator (enum)
            └── right_operand: Decimal

Operator (enum)
    ├── ADD
    ├── SUBTRACT
    ├── MULTIPLY
    └── DIVIDE

Exception Hierarchy
    └── CalculatorError
            ├── InvalidInputError
            │   └── InvalidOperatorError
            └── DivisionByZeroError
```

---

## State Transitions

**None**: All entities are immutable value objects. No state transitions occur.

The calculator is stateless:
- Each invocation creates new objects
- Objects are discarded after result is printed
- No persistence between invocations

---

## Type Safety Guarantees

All entities use strict type hints:

1. **Operator**: Enum ensures only valid operators exist
2. **Calculation**: Frozen dataclass ensures immutability
3. **Decimal**: Guarantees numeric precision per spec
4. **Exceptions**: Type-safe error handling through hierarchy

mypy strict mode validates:
- No untyped function definitions
- No implicit Any types
- Exhaustive pattern matching on enums
- Immutability through frozen dataclasses

---

## Validation Summary

| Entity | Validation Point | Error Type |
|--------|------------------|------------|
| Operator | Construction from string | InvalidOperatorError |
| Calculation | Division by zero at execution | DivisionByZeroError |
| CalculatorInput | Argument count | InvalidInputError |
| CalculatorInput | Numeric parsing | InvalidInputError |
| CalculatorInput | Operator parsing | InvalidOperatorError |

All validations occur at boundaries (input parsing) per constitution Principle VI (Clear Error Handling).
