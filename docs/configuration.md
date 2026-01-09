# Configuration Guide

MiniLangCompiler uses a small JSON configuration file plus environment
variables. This allows local, deterministic runs while still supporting AWS
uploads when desired.

## Default configuration file

The default configuration file is `config/minilang.json`:

```json
{
  "bucket": "minilang-compiler-artifacts",
  "table": "MiniLangCompilerLogs",
  "storage_dir": "out",
  "aws_mode": false
}
```

### Fields

- `bucket`: The bucket name used for compiled output.
- `table`: The DynamoDB table (or local log file) for errors.
- `storage_dir`: Base directory used in local storage mode.
- `aws_mode`: Boolean flag to enable AWS integrations.

## Environment variables

Environment variables override values in the JSON configuration file. This is
useful for CI and local overrides without editing files.

| Variable | Default | Description |
| --- | --- | --- |
| `MINILANG_BUCKET` | `minilang-compiler-artifacts` | Bucket name for compiled artifacts |
| `MINILANG_TABLE` | `MiniLangCompilerLogs` | Table name for error logs |
| `MINILANG_STORAGE_DIR` | `out` | Base output directory for local storage |
| `MINILANG_AWS_MODE` | `false` | Enable AWS mode when set to `true` |

Example:

```
export MINILANG_BUCKET=custom-bucket
export MINILANG_TABLE=CustomLogs
export MINILANG_STORAGE_DIR=./build/output
export MINILANG_AWS_MODE=false
```

## Config file override

Use the `--config` flag to specify a different configuration file:

```
python -m minilang_compiler.cli --config config/minilang.json compile examples/quickstart.minilang
```

## AWS configuration

When `aws_mode` is enabled, the compiler expects AWS credentials and region
configuration to be present. The `docs/aws.md` guide contains the full steps.

## Deterministic builds

The default configuration is intentionally deterministic: it writes outputs to
`out/` in the repo and never requires network access. This ensures both local
verification and CI runs are reproducible.

## Configuration precedence

Order of precedence:

1. CLI `--config` (if provided)
2. Environment variables
3. Default `config/minilang.json`
4. Hardcoded defaults

## Safe overrides in tests

Tests and smoke checks set `MINILANG_STORAGE_DIR` to a temporary directory to
avoid polluting local output. They do **not** modify the default config file.
