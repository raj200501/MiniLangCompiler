# Storage Format

This document describes how MiniLangCompiler stores compiled artifacts and
log entries when running in local mode. These formats are intentionally simple
and deterministic so that they can be used in tests and CI.

## Local storage layout

By default, compiled artifacts are written under `out/`.

```
out/
  s3/
    <bucket>/
      <key>.mlc
      <key>.json
  dynamodb/
    <table>.jsonl
```

- `<bucket>` defaults to `minilang-compiler-artifacts` but can be configured.
- `<key>` is derived from the input source filename stem.
- `<table>` defaults to `MiniLangCompilerLogs` but can be configured.

## Compiled artifact (`.mlc`)

The `.mlc` file is the compiled MiniLang bytecode output. Each line contains a
single instruction. Example:

```
PUSH 1
STORE x
LOAD x
PUSH 2
ADD
RETURN
```

## Metadata (`.json`)

The `.json` file holds metadata about the compilation process and is intended to
support automated checks. The schema is stable and intentionally small:

```json
{
  "bucket": "minilang-compiler-artifacts",
  "key": "quickstart",
  "instructions": [
    "PUSH 40",
    "STORE x",
    "PUSH 2",
    "STORE y",
    "LOAD x",
    "LOAD y",
    "ADD",
    "STORE z",
    "LOAD z",
    "PUSH 2",
    "MUL",
    "RETURN"
  ]
}
```

### Fields

- `bucket`: The configured bucket name.
- `key`: The object key (input filename stem).
- `instructions`: The rendered instructions emitted by the compiler.

## Error log (`.jsonl`)

Errors are logged to a JSON Lines file. Each line is a JSON object with the
following shape:

```json
{
  "table": "MiniLangCompilerLogs",
  "key": "quickstart.minilang",
  "message": "SemanticError: Unbound variable 'x' at line 3, column 1",
  "timestamp": "2024-01-01T00:00:00+00:00"
}
```

### Fields

- `table`: The configured table name.
- `key`: The source file name.
- `message`: The error message, including location data.
- `timestamp`: UTC timestamp in ISO 8601 format.

## AWS mode

When `MINILANG_AWS_MODE=true`, the compiler uses boto3 to store the same `.mlc`
and `.json` content in AWS S3, and errors are stored in AWS DynamoDB. The storage
format is identical, but AWS mode is not used in the automated tests to keep the
project deterministic and self-contained.

## Backward compatibility

The storage format is versionless by design. If you extend MiniLang with new
features, consider adding optional fields to the metadata JSON rather than
changing the existing keys.
