# Tasks: Basic CLI Calculator

**Input**: Design documents from `/specs/001-cli-calculator/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Tests are REQUIRED per constitution Principle III (Test-First Development). All tests must be written and approved BEFORE implementation begins.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (this project)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure: src/calculator/, tests/unit/, tests/integration/
- [x] T002 Initialize Python project with UV: create pyproject.toml with Python 3.11+ requirement
- [x] T003 Create .python-version file specifying Python 3.11
- [x] T004 [P] Configure UV dev dependencies: pytest>=7.4.0, pytest-cov>=4.1.0, mypy>=1.5.0, ruff>=0.1.0
- [x] T005 [P] Create mypy.ini with strict mode configuration
- [x] T006 [P] Create ruff configuration in pyproject.toml (line-length=100, target-version=py311)
- [x] T007 [P] Create README.md with project overview and usage instructions

**Checkpoint**: Project structure ready, tools configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 [P] Create custom exceptions in src/calculator/exceptions.py with type hints
- [x] T009 [P] Write unit tests for exceptions in tests/unit/test_exceptions.py
- [x] T010 Create Operator enum in src/calculator/operations.py with symbol property and from_string classmethod
- [x] T011 Create package initialization in src/calculator/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Arithmetic Operations (Priority: P1) 🎯 MVP

**Goal**: Users can perform basic arithmetic calculations (addition, subtraction, multiplication, division) with positive integers through CLI

**Independent Test**: Run calculator with two positive integers and each operator (+, -, *, /) and verify correct results

### Tests for User Story 1 (Test-First Development - RED Phase)

> **NOTE: Write these tests FIRST, get user approval, ensure they FAIL before implementation**

- [x] T012 [P] [US1] Write unit tests for add function with positive integers in tests/unit/test_operations.py
- [x] T013 [P] [US1] Write unit tests for subtract function with positive integers in tests/unit/test_operations.py
- [x] T014 [P] [US1] Write unit tests for multiply function with positive integers in tests/unit/test_operations.py
- [x] T015 [P] [US1] Write unit tests for divide function with positive integers in tests/unit/test_operations.py
- [x] T016 [P] [US1] Write unit tests for divide by zero error in tests/unit/test_operations.py
- [x] T017 [P] [US1] Write unit tests for parser with valid 3-argument input in tests/unit/test_parser.py
- [x] T018 [P] [US1] Write unit tests for parser with invalid input (wrong count, invalid operator) in tests/unit/test_parser.py
- [x] T019 [US1] Write integration tests for CLI end-to-end with positive integers in tests/integration/test_cli.py
- [x] T020 [US1] Run pytest to verify all tests FAIL (RED) - get user approval to proceed

### Implementation for User Story 1 (GREEN Phase)

- [x] T021 [P] [US1] Implement add function in src/calculator/operations.py with type hints (Decimal → Decimal)
- [x] T022 [P] [US1] Implement subtract function in src/calculator/operations.py with type hints
- [x] T023 [P] [US1] Implement multiply function in src/calculator/operations.py with type hints
- [x] T024 [P] [US1] Implement divide function in src/calculator/operations.py with type hints and DivisionByZeroError
- [x] T025 [US1] Create Calculation value object in src/calculator/operations.py as frozen dataclass
- [x] T026 [US1] Implement Calculation.execute() method dispatching to operation functions
- [x] T027 [US1] Create CalculatorInput value object in src/calculator/parser.py as frozen dataclass
- [x] T028 [US1] Implement CalculatorInput.parse() classmethod with validation in src/calculator/parser.py
- [x] T029 [US1] Create CLI entry point main() in src/calculator/cli.py with sys.argv handling
- [x] T030 [US1] Implement error handling in main() catching CalculatorError and printing to stderr
- [x] T031 [US1] Implement result formatting (normalize Decimal, remove trailing zeros) in src/calculator/cli.py
- [x] T032 [US1] Create __main__.py entry point calling cli.main()
- [x] T033 [US1] Add usage message display when no arguments provided in src/calculator/cli.py
- [x] T034 [US1] Run pytest to verify all US1 tests PASS (GREEN)
- [x] T035 [US1] Run mypy src/ to verify type safety compliance
- [x] T036 [US1] Run ruff check and ruff format on all code

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently with positive integers

---

## Phase 4: User Story 2 - Decimal Number Support (Priority: P2)

**Goal**: Users can perform calculations with decimal numbers for real-world scenarios requiring precision

**Independent Test**: Run calculations with decimal numbers (e.g., "3.5 + 2.1", "10.5 / 2") and verify accurate results

### Tests for User Story 2 (Test-First Development - RED Phase)

- [x] T037 [P] [US2] Write unit tests for operations with decimal operands in tests/unit/test_operations.py
- [x] T038 [P] [US2] Write unit tests for decimal precision (0.1 + 0.2 = 0.3) in tests/unit/test_operations.py
- [x] T039 [P] [US2] Write unit tests for parser accepting decimal number strings in tests/unit/test_parser.py
- [x] T040 [US2] Write integration tests for CLI with decimal numbers in tests/integration/test_cli.py
- [x] T041 [US2] Run pytest to verify US2 tests FAIL (RED) - get user approval to proceed

### Implementation for User Story 2 (GREEN Phase)

- [x] T042 [US2] Update parser to handle decimal strings using Decimal() constructor in src/calculator/parser.py
- [x] T043 [US2] Add InvalidInputError for non-parseable decimal strings in src/calculator/parser.py
- [x] T044 [US2] Update result formatting to handle decimal display precision in src/calculator/cli.py
- [x] T045 [US2] Run pytest to verify all US2 tests PASS (GREEN)
- [x] T046 [US2] Run mypy and ruff to verify code quality

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (positive integers + decimals)

---

## Phase 5: User Story 3 - Negative Number Handling (Priority: P3)

**Goal**: Users can perform calculations involving negative numbers for complete mathematical coverage

**Independent Test**: Run calculations with negative numbers (e.g., "-5 + 3", "10 - -4") and verify mathematical correctness

### Tests for User Story 3 (Test-First Development - RED Phase)

- [x] T047 [P] [US3] Write unit tests for operations with negative operands in tests/unit/test_operations.py
- [x] T048 [P] [US3] Write unit tests for negative result cases in tests/unit/test_operations.py
- [x] T049 [P] [US3] Write unit tests for parser accepting negative number strings in tests/unit/test_parser.py
- [x] T050 [US3] Write integration tests for CLI with negative numbers in tests/integration/test_cli.py
- [x] T051 [US3] Run pytest to verify US3 tests FAIL (RED) - get user approval to proceed

### Implementation for User Story 3 (GREEN Phase)

- [x] T052 [US3] Update parser to correctly handle negative number parsing (distinguish "-" operator from negative sign) in src/calculator/parser.py
- [x] T053 [US3] Verify negative number support in all operations (already handled by Decimal, but test edge cases)
- [x] T054 [US3] Run pytest to verify all US3 tests PASS (GREEN)
- [x] T055 [US3] Run mypy and ruff to verify code quality

**Checkpoint**: All user stories should now be independently functional (positive, decimal, negative numbers)

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and finalization

- [x] T056 [P] Add docstrings to all public functions and classes per constitution documentation standards
- [x] T057 [P] Run pytest --cov=calculator --cov-report=term-missing to verify 90%+ coverage
- [x] T058 [P] Update README.md with complete installation and usage examples from quickstart.md
- [x] T059 [P] Create .gitignore for Python (__pycache__, .venv, .mypy_cache, .pytest_cache, .coverage)
- [x] T060 [US1] Validate quickstart.md examples by running them manually
- [x] T061 Perform final mypy strict mode check across entire codebase
- [x] T062 Perform final ruff check and format across entire codebase
- [x] T063 Run full test suite and verify <1 second execution time per constitution requirement

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3)
  - Each story extends previous functionality without breaking it
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Extends US1 by adding decimal support - Can reuse all US1 code
- **User Story 3 (P3)**: Extends US1+US2 by adding negative support - Can reuse all previous code

### Within Each User Story (Test-First Workflow)

1. **RED Phase**: Write tests FIRST
   - All test tasks marked [P] can run in parallel
   - Must get user approval on test cases
   - Run pytest to verify tests FAIL
2. **GREEN Phase**: Implement to pass tests
   - Implementation tasks have dependencies (operations → Calculation → parser → CLI)
   - Run pytest frequently to verify progress
3. **REFACTOR Phase**: Clean up code (happens in Polish phase)

### Parallel Opportunities

**Phase 1 (Setup)**:
- T004, T005, T006, T007 can all run in parallel (different files)

**Phase 2 (Foundational)**:
- T008 and T009 can run in parallel (exceptions and their tests)

**Phase 3 (US1 Tests - RED)**:
- T012, T013, T014, T015, T016 can run in parallel (different test functions in same file)
- T017, T018 can run in parallel (different test functions)

**Phase 3 (US1 Implementation - GREEN)**:
- T021, T022, T023, T024 can run in parallel (separate functions in operations.py)

**Phase 4 (US2 Tests)**:
- T037, T038, T039 can run in parallel

**Phase 5 (US3 Tests)**:
- T047, T048, T049 can run in parallel

**Phase 6 (Polish)**:
- T056, T057, T058, T059 can run in parallel

---

## Parallel Example: User Story 1 (RED Phase)

```bash
# Launch all operation tests together:
Task T012: "Write unit tests for add function"
Task T013: "Write unit tests for subtract function"
Task T014: "Write unit tests for multiply function"
Task T015: "Write unit tests for divide function"
Task T016: "Write unit test for divide by zero"

# Launch parser tests together:
Task T017: "Write unit tests for valid input parsing"
Task T018: "Write unit tests for invalid input parsing"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T011) - CRITICAL
3. Complete Phase 3: User Story 1 (T012-T036)
   - RED: Write tests first (T012-T020)
   - GREEN: Implement to pass tests (T021-T036)
4. **STOP and VALIDATE**: Test US1 independently with positive integers
5. Deploy/demo MVP if ready

**MVP Scope**: Basic calculator with four operations, positive integers only, error handling, exit codes

### Incremental Delivery

1. **Setup + Foundational** (T001-T011) → Foundation ready
2. **Add US1** (T012-T036) → Test independently → **Deploy MVP** (basic arithmetic with positive integers)
3. **Add US2** (T037-T046) → Test independently → Deploy v1.1 (decimal support added)
4. **Add US3** (T047-T055) → Test independently → Deploy v1.2 (negative numbers added)
5. **Polish** (T056-T063) → Production-ready v1.0

Each story adds value without breaking previous stories.

### Sequential Strategy (Recommended)

This project's user stories build on each other incrementally:

1. Complete Setup + Foundational together (T001-T011)
2. **User Story 1**: Full TDD cycle (T012-T036)
   - Delivers basic calculator MVP
   - Can stop here for minimal viable product
3. **User Story 2**: Extend with decimals (T037-T046)
   - Reuses all US1 code, just updates parser and formatting
4. **User Story 3**: Extend with negatives (T047-T055)
   - Reuses all previous code, just updates parser
5. **Polish**: Finalize documentation and quality (T056-T063)

---

## Constitution Compliance Validation

### Principle III: Test-First Development

Each user story follows strict Red-Green-Refactor:

**RED Phase**:
- Tasks T012-T020 (US1): Write tests, verify FAIL
- Tasks T037-T041 (US2): Write tests, verify FAIL
- Tasks T047-T051 (US3): Write tests, verify FAIL

**GREEN Phase**:
- Tasks T021-T036 (US1): Implement, verify PASS
- Tasks T042-T046 (US2): Implement, verify PASS
- Tasks T052-T055 (US3): Implement, verify PASS

**REFACTOR Phase**:
- Phase 6: Polish and cleanup

### Type Safety Validation

- T035, T046, T055, T061: mypy strict mode checks at each story completion

### Code Quality Validation

- T036, T046, T055, T062: ruff linting and formatting at each story completion

---

## Notes

- [P] tasks = different files or independent functions, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story builds incrementally on previous stories
- User approval required before moving from RED to GREEN phase per constitution
- Commit after completing each phase (Setup, Foundational, US1, US2, US3, Polish)
- Stop at any checkpoint to validate story independently
- All file paths are absolute from repository root
