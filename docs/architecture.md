# Architecture Overview

This document explains how the MiniLangCompiler Python implementation is
organized. It is intended for maintainers and contributors.

## High-level flow

1. **Read source** (`minilang_compiler.compiler.compile_file`)
2. **Tokenize** (`minilang_compiler.lexer.tokenize`)
3. **Parse** (`minilang_compiler.parser.parse`)
4. **Semantic analysis** (`minilang_compiler.semant.analyze`)
5. **Code generation** (`minilang_compiler.codegen.generate`)
6. **Storage** (`minilang_compiler.storage.LocalStorage` or `AwsStorage`)

Errors in steps 2–4 are reported through the storage backend as log entries.

## Package map

```
src/minilang_compiler/
  ast.py        # AST nodes, tokens, source locations
  lexer.py      # tokenization logic
  parser.py     # recursive descent parser
  semant.py     # semantic analysis and warnings
  codegen.py    # stack-based instruction generation
  storage.py    # local/AWS storage backends
  config.py     # configuration loader
  compiler.py   # orchestration logic
  cli.py        # CLI entrypoint
```

## AST

The AST model is defined in `ast.py` and focuses on a minimal set of expression
nodes: integer literals, variables, and binary operators. Each node carries a
`SourceLocation` for error reporting.

The AST is immutable (dataclasses with `frozen=True`), which simplifies
reasoning about transformations.

## Lexer

The lexer is a small state machine that consumes characters and emits tokens
with line/column metadata. The lexer recognizes:

- integer literals
- identifiers
- arithmetic operators
- parentheses
- semicolons
- comments (`#` and `//`)

Any unknown character raises `LexerError`.

## Parser

The parser is a recursive descent parser. It expects the program to begin with
`let`, followed by a semicolon-delimited declaration list, then `in`, and a
single expression.

Operator precedence is enforced with separate parsing methods:

- `_parse_expr` for `+`/`-`
- `_parse_term` for `*`/`/`
- `_parse_factor` for literals, identifiers, and parenthesized expressions

## Semantic analysis

The semantic phase checks the following invariants:

- No duplicate declarations.
- All variables are declared before use.
- Division by literal zero is rejected.

Warnings are emitted for declared-but-unused variables. The compiler does not
halt for warnings, but prints them when using the CLI.

## Code generation

The code generator emits a small stack machine instruction set:

- `PUSH <int>`
- `LOAD <name>`
- `STORE <name>`
- `ADD`, `SUB`, `MUL`, `DIV`
- `RETURN`

This instruction stream is stored in text form and also serialized to JSON for
metadata. The compiler also exposes `interpret()` for running a MiniLang AST
without executing bytecode.

## Storage

MiniLangCompiler supports two storage backends:

1. **LocalStorage** writes compiled output under `out/s3/<bucket>/` and logs
   errors to `out/dynamodb/<table>.jsonl`.
2. **AwsStorage** uses boto3 clients to upload the same artifacts to AWS S3 and
   DynamoDB, respectively.

The storage backend is selected by configuration in `Config`. The defaults are
local storage to keep the project self-contained and deterministic for testing.

## Configuration

Configuration is loaded from `config/minilang.json` by default, but can be
overridden via environment variables or the `--config` CLI flag.

Key options:

- `bucket` / `MINILANG_BUCKET`
- `table` / `MINILANG_TABLE`
- `storage_dir` / `MINILANG_STORAGE_DIR`
- `aws_mode` / `MINILANG_AWS_MODE`

## CLI

The CLI is built on Python's `argparse` and exposes three commands:

- `compile <file>`: compile and store bytecode.
- `run <file>`: compile, then interpret and print the result.
- `check <file>`: parse and run semantic analysis only.

The CLI uses `minilang_compiler.compiler` to avoid duplicating logic.

## Tests

The test suite uses the standard library `unittest` framework and covers:

- Lexing (tokenization) scenarios
- Parser correctness and error paths
- Semantic checks and warnings
- Code generation and interpretation
- Local storage behavior
- CLI integration for compile/run

In addition to unit tests, `scripts/smoke_test.py` runs a full compile+run cycle
against `examples/quickstart.minilang` and validates generated artifacts.

## Release workflow

The canonical verification command is `./scripts/verify.sh`. It sets up a virtual
environment, installs dependencies, runs the test suite, and executes the smoke
test. GitHub Actions invokes the same script to guarantee parity between local
and CI verification.
