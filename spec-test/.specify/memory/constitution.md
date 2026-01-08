<!--
SYNC IMPACT REPORT:
Version change: [NONE] → 1.0.0 (Initial constitution)
Modified principles: N/A (Initial creation)
Added sections:
  - Core Principles (I-VI)
  - Code Quality Standards
  - Development Workflow
  - Governance
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section references this file
  ✅ spec-template.md - Requirements align with principles
  ✅ tasks-template.md - Task categorization aligns with principles
Follow-up TODOs: None
-->

# Python Calculator Constitution

## Core Principles

### I. Type Safety First

**All Python code MUST use type hints.**

Type hints are mandatory for all function signatures, class attributes, and module-level variables. This ensures code clarity, enables static analysis, and catches errors before runtime.

**Rationale**: Type hints improve code maintainability, enable better IDE support, catch bugs early through static analysis (mypy), and serve as inline documentation for developers.

### II. Dependency Management with UV

**Project dependencies MUST be managed exclusively through UV.**

All package installation, virtual environment creation, and dependency resolution will use UV. No mixing with pip, poetry, or other package managers.

**Rationale**: UV provides faster, more reliable dependency resolution. Standardizing on a single tool prevents version conflicts and ensures reproducible builds across environments.

### III. Test-First Development (NON-NEGOTIABLE)

**Tests MUST be written and approved before implementation begins.**

Follow strict Red-Green-Refactor cycle:
1. Write tests that define expected behavior
2. Get user approval on test cases
3. Verify tests fail (Red)
4. Implement code to pass tests (Green)
5. Refactor while keeping tests green

**Rationale**: Test-first development ensures requirements are clear, prevents scope creep, and creates living documentation. Tests define success criteria before implementation bias occurs.

### IV. Simplicity and YAGNI

**Implement only what is explicitly required. No speculative features.**

Start with the simplest solution that meets requirements. Avoid:
- Premature abstractions
- Unused configuration options
- "Future-proof" complexity
- Framework overkill for simple problems

**Rationale**: Complexity is a liability. Simple code is easier to understand, test, maintain, and debug. Additional features can be added when actually needed, not when hypothetically useful.

### V. Pure Functions and Testability

**Favor pure functions with clear inputs and outputs.**

Functions should:
- Take explicit parameters (no hidden dependencies)
- Return values rather than modify state
- Avoid side effects where possible
- Be independently testable

**Rationale**: Pure functions are predictable, easy to test, and can be reasoned about in isolation. This aligns with the calculator domain where operations are mathematical transformations.

### VI. Clear Error Handling

**All error conditions MUST be explicitly handled with clear error messages.**

Use Python's type system and exception hierarchy appropriately:
- Validate inputs at boundaries
- Raise specific exception types
- Provide actionable error messages
- Document expected exceptions in docstrings

**Rationale**: Clear error handling prevents silent failures, aids debugging, and improves user experience. Error messages should guide users toward solutions.

## Code Quality Standards

### Static Analysis

All code MUST pass:
- **mypy** for type checking (strict mode)
- **ruff** for linting and formatting
- No warnings or errors allowed in CI/CD

### Testing Standards

- Unit tests for all functions
- Test edge cases and error conditions
- Test coverage target: 90%+
- Tests MUST be fast (<1 second per test suite)

### Documentation

- Docstrings for all public functions and classes
- Clear parameter and return type descriptions
- Usage examples for complex operations
- Keep documentation close to code (avoid separate docs that drift)

## Development Workflow

### Branch Strategy

- `main` branch is always deployable
- Feature branches follow pattern: `###-feature-name`
- All changes via pull requests
- Squash commits on merge

### Commit Standards

- Commits MUST be atomic (one logical change)
- Clear commit messages following conventional commits
- Reference issue/task numbers where applicable

### Code Review

- All code requires review before merge
- Reviewer verifies:
  - Constitution compliance
  - Tests pass and cover edge cases
  - Type hints present and correct
  - Simplicity maintained (no unnecessary complexity)

## Governance

This constitution supersedes all other development practices. When in doubt, defer to these principles.

### Amendment Process

Constitution changes require:
1. Documented justification
2. Team review and approval
3. Version increment (semantic versioning)
4. Migration plan if changes affect existing code

### Compliance

- All PRs MUST verify constitution compliance
- Complexity MUST be justified against Principle IV (Simplicity)
- Violations require explicit approval with documented rationale

### Runtime Guidance

For detailed implementation guidance during development, see `CLAUDE.md` in the repository root.

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
