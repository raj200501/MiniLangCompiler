# CLI Reference

The MiniLangCompiler CLI is implemented in `minilang_compiler.cli`. The binary
name used in documentation is `minilangc`, but you invoke it via `python -m` or
`./scripts/run.sh` in this repository.

## Command synopsis

```
python -m minilang_compiler.cli [--config <config.json>] <command> <source>
```

Commands:

- `compile`: Compile a MiniLang file and store artifacts.
- `run`: Compile, then interpret the program and print the result.
- `check`: Parse and validate the program without emitting bytecode.

## Common flags

### `--config`

Override the default configuration file. By default, the compiler reads
`config/minilang.json`. You can provide a custom config file that follows the
same schema.

Example:

```
python -m minilang_compiler.cli --config config/minilang.json compile examples/quickstart.minilang
```

## compile

```
python -m minilang_compiler.cli compile examples/quickstart.minilang
```

Output:

- Prints a success message.
- Writes compiled bytecode to `out/s3/<bucket>/<key>.mlc`.
- Writes metadata to `out/s3/<bucket>/<key>.json`.

## run

```
python -m minilang_compiler.cli run examples/quickstart.minilang
```

Output:

- Prints a success message.
- Prints the interpreted result (`Result: <value>`).
- Writes compiled bytecode artifacts (same as `compile`).

## check

```
python -m minilang_compiler.cli check examples/quickstart.minilang
```

Output:

- Prints a success message.
- Prints the declared symbols.
- Does **not** write compiled output.

## Warnings

The CLI prints warnings for unused variables. Warnings do not cause a failure.
If you want stricter behavior, run the compiler logic directly and treat
warnings as errors.

## Exit codes

- `0` on success.
- `1` on any compilation failure.

## Examples

Compile a program:

```
./scripts/run.sh examples/quickstart.minilang compile
```

Compile and run a program:

```
./scripts/run.sh examples/quickstart.minilang run
```

Check a program without output:

```
./scripts/run.sh examples/quickstart.minilang check
```

## Environment variables

The CLI honors these environment variables (also configurable in
`config/minilang.json`):

- `MINILANG_BUCKET`: output bucket name.
- `MINILANG_TABLE`: error log table name.
- `MINILANG_STORAGE_DIR`: base output directory.
- `MINILANG_AWS_MODE`: `true` to enable AWS upload.

Set them before invoking the CLI:

```
export MINILANG_STORAGE_DIR=out
export MINILANG_BUCKET=minilang-compiler-artifacts
export MINILANG_TABLE=MiniLangCompilerLogs
```

## Exit code usage in CI

CI uses `./scripts/verify.sh`, which runs the CLI in smoke tests. Any non-zero
exit code will fail the workflow. This ensures the CLI remains reliable and
compatible with the documented behavior.
