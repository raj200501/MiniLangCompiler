# Testing Guide

MiniLangCompiler includes unit tests and a smoke test that validate the README
contract. This guide describes how to run and interpret the tests.

## Quickstart

Run the full verification suite:

```
./scripts/verify.sh
```

This command:

1. Creates a Python virtual environment in `.venv`.
2. Runs the `unittest` test suite.
3. Executes `scripts/smoke_test.py` for an end-to-end check.

## Unit tests

Unit tests live in `tests/` and cover the following components:

- Lexer tokenization
- Parser correctness
- Semantic analysis and error conditions
- Code generation and interpreter behavior
- Local storage functionality
- CLI integration (compile and run)

Run them directly with:

```
PYTHONPATH=src python -m unittest discover -s tests -p "test_*.py"
```

## Smoke test

The smoke test uses the CLI to compile and run `examples/quickstart.minilang`.
It asserts that:

- The CLI returns exit code 0.
- The compiled `.mlc` file exists in `out/`.
- The metadata JSON contains a `RETURN` instruction.

Run it directly with:

```
PYTHONPATH=src python scripts/smoke_test.py
```

## Adding tests

When extending the compiler:

1. Add unit tests in `tests/` for any new parser, semantic, or codegen logic.
2. Update the smoke test if the CLI contract changes.
3. Update the README Verified Verification section.

## Determinism requirements

Tests must not rely on network access or external services. The local storage
backend ensures deterministic outputs. AWS integration is **not** used in tests.

## Debugging failures

When a test fails:

- Inspect the failing test file in `tests/`.
- Run the specific test module with `python -m unittest tests.test_parser`.
- Use `PYTHONPATH=src` to ensure the compiler package is importable.
- Check that example files in `examples/` are unmodified.

## Coverage goals

While there is no strict coverage requirement, the test suite should cover all
compiler phases and the CLI. Use descriptive test names and favor integration
coverage over brittle implementation details.
