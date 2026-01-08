# Implementation Plan: Basic CLI Calculator

**Branch**: `001-cli-calculator` | **Date**: 2026-01-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-calculator/spec.md`

## Summary

Build a command-line calculator that performs basic arithmetic operations (addition, subtraction, multiplication, division) with support for positive integers, decimal numbers, and negative numbers. The calculator will validate inputs, handle edge cases like division by zero, and provide clear error messages. Technical approach uses Python with type hints, pytest for testing, and UV for dependency management.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (stdlib only for core functionality), pytest for testing, mypy for type checking, ruff for linting
**Storage**: N/A (stateless calculator)
**Testing**: pytest with 90%+ coverage target
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single project (CLI application)
**Performance Goals**: Sub-1-second calculation time (per spec SC-001)
**Constraints**: Must use type hints (constitution), test-first development (constitution), UV for dependency management (constitution)
**Scale/Scope**: Single-user CLI tool, simple arithmetic operations, no persistent state

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle I: Type Safety First
- **Status**: COMPLIANT
- **Implementation**: All functions will use type hints for parameters and return values
- **Validation**: mypy strict mode will enforce type safety

### ✅ Principle II: Dependency Management with UV
- **Status**: COMPLIANT
- **Implementation**: Project will use UV for all dependency management
- **Validation**: pyproject.toml will be managed by UV

### ✅ Principle III: Test-First Development
- **Status**: COMPLIANT
- **Implementation**: Tests will be written before implementation for each user story
- **Validation**: Red-Green-Refactor cycle documented in tasks

### ✅ Principle IV: Simplicity and YAGNI
- **Status**: COMPLIANT
- **Implementation**: No external dependencies for core logic, stdlib only
- **Justification**: Calculator operations are pure mathematical functions that don't require frameworks
- **Avoided**: Expression parsing libraries, GUI frameworks, configuration systems

### ✅ Principle V: Pure Functions and Testability
- **Status**: COMPLIANT
- **Implementation**: All arithmetic operations will be pure functions (input → output, no side effects)
- **Validation**: Each operation independently testable with clear I/O

### ✅ Principle VI: Clear Error Handling
- **Status**: COMPLIANT
- **Implementation**: Custom exception types for domain errors (DivisionByZeroError, InvalidInputError)
- **Validation**: All error scenarios from spec have defined error messages

### Code Quality Standards
- **mypy strict mode**: ✅ Enabled
- **ruff**: ✅ Enabled for linting and formatting
- **pytest coverage**: ✅ Target 90%+
- **Test speed**: ✅ Expected <1s for entire suite (simple operations)

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-calculator/
├── plan.md              # This file
├── research.md          # Phase 0 output - Python best practices for CLI
├── data-model.md        # Phase 1 output - Domain model
├── quickstart.md        # Phase 1 output - Usage guide
└── checklists/
    └── requirements.md  # Already created during spec phase
```

### Source Code (repository root)

```text
src/
├── calculator/
│   ├── __init__.py      # Package initialization
│   ├── operations.py    # Pure arithmetic functions (add, subtract, multiply, divide)
│   ├── parser.py        # Input parsing and validation
│   ├── exceptions.py    # Custom exception types
│   └── cli.py           # CLI entry point and argument handling
└── __main__.py          # Main entry point (python -m calculator)

tests/
├── unit/
│   ├── test_operations.py     # Unit tests for arithmetic operations
│   ├── test_parser.py         # Unit tests for input parsing
│   └── test_exceptions.py     # Unit tests for error handling
└── integration/
    └── test_cli.py            # Integration tests for CLI end-to-end

pyproject.toml           # Project metadata and dependencies (UV-managed)
.python-version          # Python version specification
README.md                # Project documentation
```

**Structure Decision**: Single project structure selected because this is a standalone CLI tool with no web/mobile components. Structure follows Python best practices with separate modules for concerns (operations, parsing, CLI), enabling independent testing of each component per constitution Principle V.

## Complexity Tracking

No violations detected. All constitution principles satisfied with simple design choices.

---

## Phase 0: Research Complete ✅

**Output**: [research.md](./research.md)

**Key Decisions**:
- Python 3.11+ for performance and type hints
- Decimal type for precision (avoids float errors)
- sys.argv for CLI parsing (no framework needed)
- Custom exception hierarchy for domain errors
- pytest for testing, mypy strict for type checking, ruff for linting

All research findings support constitution compliance.

---

## Phase 1: Design Complete ✅

**Outputs**:
- [data-model.md](./data-model.md) - Domain model with Operator enum, Calculation value object, exception hierarchy
- [quickstart.md](./quickstart.md) - End-user documentation with examples and troubleshooting

**Architecture**:
- Immutable value objects (Operator, Calculation, CalculatorInput)
- Pure functions for arithmetic operations
- Clear separation: operations.py, parser.py, exceptions.py, cli.py
- Type-safe error handling through custom exceptions

**Constitution Re-Check**: ✅ ALL PRINCIPLES COMPLIANT

Post-design validation confirms:
- Type safety: All entities use strict type hints with mypy enforcement
- Simplicity: No external dependencies, stdlib-only implementation
- Testability: Pure functions enable isolated unit testing
- Clear errors: Custom exception hierarchy with spec-defined messages
- UV ready: pyproject.toml structure defined for UV management
- Test-first: Architecture supports TDD with clear test boundaries

---

## Next Steps

This plan is complete. Ready for task generation:

```bash
/sp.tasks
```

The tasks command will generate a detailed task list organized by user story (P1: basic ops, P2: decimals, P3: negatives) with test-first workflow.
