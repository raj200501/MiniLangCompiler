# MiniLangCompiler

**MiniLangCompiler** is a deterministic compiler for a small domain-specific
language (DSL) named **MiniLang**. The compiler performs lexical analysis,
parsing, semantic checks, and code generation, then stores compiled bytecode and
metadata in a local, S3-compatible layout. Optional AWS integrations allow the
same artifacts to be uploaded to real S3 and logged to DynamoDB.

The canonical implementation in this repository is the Python compiler in
`src/minilang_compiler/`. The original OCaml prototype remains in `src/` for
reference, but the Python tooling is what the scripts and CI use.

## Features

- Lexer, parser, semantic analysis, and code generation for MiniLang
- Stack-based bytecode output with JSON metadata
- Local S3/DynamoDB emulation for deterministic artifacts
- Optional AWS S3 + DynamoDB uploads (disabled by default)
- CLI to compile, run, and check MiniLang programs

## Installation

This repository is self-contained and requires only Python 3.11+.

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/MiniLangCompiler.git
    cd MiniLangCompiler
    ```

2. (Optional) Set up a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

## Usage

MiniLang programs start with a `let` block and end with an `in` expression.
Example:

```minilang
let x = 40;
    y = 2;
    z = x + y
in
  z * 2
```

### Compile

```bash
./scripts/run.sh examples/quickstart.minilang compile
```

Expected output includes:

- `out/s3/minilang-compiler-artifacts/quickstart.mlc` (bytecode)
- `out/s3/minilang-compiler-artifacts/quickstart.json` (metadata)

### Run (compile + interpret)

```bash
./scripts/run.sh examples/quickstart.minilang run
```

Expected output:

- `Result: 84`
- Compiled artifacts stored in `out/` (same as compile)

### Check (parse + semantic analysis only)

```bash
./scripts/run.sh examples/quickstart.minilang check
```

## Verified Quickstart (commands executed)

```bash
./scripts/run.sh examples/quickstart.minilang run
```

## Verification

Run the canonical verification script:

```bash
./scripts/verify.sh
```

## Verified Verification (commands executed)

```bash
./scripts/verify.sh
```

## Configuration

Configuration is loaded from `config/minilang.json` by default and can be
overridden with environment variables. See `docs/configuration.md` for details.

## AWS integration (optional)

AWS mode is disabled by default. To enable it, install boto3 and set
`MINILANG_AWS_MODE=true`. Full instructions are in `docs/aws.md`.

## Repository docs

- `docs/language.md` — MiniLang language specification
- `docs/architecture.md` — Compiler architecture overview
- `docs/cli.md` — CLI reference
- `docs/testing.md` — Testing guide
- `docs/storage-format.md` — Output format details
- `docs/troubleshooting.md` — Common issues

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
