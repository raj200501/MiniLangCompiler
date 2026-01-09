# Troubleshooting

This document covers common issues when running or verifying MiniLangCompiler.

## Python not found

The scripts rely on `python3` being available. On most Linux distributions,
`python3` is installed by default. If not, install it from your package manager
and re-run `./scripts/verify.sh`.

## Virtual environment issues

If the virtual environment becomes corrupted, delete the `.venv/` directory and
re-run `./scripts/verify.sh`. The scripts will recreate the environment.

```
rm -rf .venv
./scripts/verify.sh
```

## Permission denied when running scripts

Make sure the scripts are executable:

```
chmod +x scripts/run.sh scripts/verify.sh scripts/bootstrap.sh
```

## Compilation failed

When compilation fails, the error is written to `out/dynamodb/<table>.jsonl`. The
message includes file/line/column information.

Example log entry:

```json
{
  "table": "MiniLangCompilerLogs",
  "key": "example.minilang",
  "message": "SemanticError: Unbound variable 'x' at line 4, column 1",
  "timestamp": "2024-01-01T00:00:00+00:00"
}
```

Common causes:

- Missing semicolons between declarations.
- Referencing a variable before it is declared.
- Typographical errors in variable names.

## AWS mode errors

AWS mode requires boto3 and valid AWS credentials. If you see an error like
"AWS mode requires boto3", install boto3:

```
python -m pip install boto3
```

Then set environment variables:

```
export MINILANG_AWS_MODE=true
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=...
```

## Test failures

The test suite exercises the compiler and CLI. If tests fail:

1. Run `./scripts/verify.sh` to ensure dependencies are installed.
2. Inspect the test output in `tests/` to find the failing expectation.
3. Verify that `examples/quickstart.minilang` has not been modified unexpectedly.

## Integration test failure

`scripts/smoke_test.py` validates that the CLI can compile and run the
quickstart example and that the output artifacts exist. Ensure the `out/`
directory is writable and that the Python package is importable via
`PYTHONPATH=src`.

## Windows support

Windows is not officially supported in CI. If you need to run the project on
Windows, consider using WSL2 and follow the Linux instructions.
