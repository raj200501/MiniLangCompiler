# Extension Guide

MiniLangCompiler is intentionally small, but it is structured to allow future
language extensions. This guide outlines how to add new language features while
keeping the compiler pipeline consistent.

## Adding new tokens

1. Update `minilang_compiler.ast.TokenKind` with the new token kind.
2. Extend `minilang_compiler.lexer.SINGLE_CHAR_TOKENS` or keyword list as needed.
3. Add lexer tests in `tests/test_lexer.py` to cover the new token.

## Adding new AST nodes

Add a new dataclass in `minilang_compiler.ast` for the expression or statement.
Remember to include a `SourceLocation` and implement a `pretty()` method for
human-readable debugging.

## Parser updates

Extend the parser in `minilang_compiler.parser`:

- Create a new parsing method if the grammar grows in complexity.
- Update `_parse_factor` if the new node fits as a factor.
- Add parser tests in `tests/test_parser.py` to validate both success and error
  paths.

## Semantic analysis

Update `minilang_compiler.semant` to enforce new rules. For example, if you add
boolean expressions, ensure type checking rejects mixed boolean/integer usage.

Add tests in `tests/test_semant.py` to cover the new semantics.

## Code generation

Update `minilang_compiler.codegen` to emit instructions for the new node. If you
extend the instruction set:

- Update the `Instruction` render logic if needed.
- Add tests that validate the emitted instruction sequence.
- Update `docs/language.md` with the new feature.

## Interpreter support

The interpreter in `minilang_compiler.codegen.interpret` should mirror the
semantics of the compiler. Whenever you add a node or operator, extend the
interpreter to evaluate it and add tests to ensure interpreter results match
expected output.

## Storage changes

If you add new metadata fields, update `minilang_compiler.storage` and
`docs/storage-format.md` to reflect the new schema. Try to preserve backward
compatibility by adding optional fields instead of modifying existing ones.

## CLI changes

Update `minilang_compiler.cli` to expose new commands or flags. Ensure the README
and `docs/cli.md` are updated, and add integration tests in `tests/test_cli.py`.

## Verification updates

If the README contract changes, update:

- `scripts/smoke_test.py` to reflect the new behavior.
- `docs/testing.md` if needed.
- `README.md` Verified Quickstart/Verification sections.

## Example: adding boolean literals

1. Add `BOOL` token in `TokenKind`.
2. Extend lexer to read `true`/`false` keywords.
3. Add `BoolLiteral` AST node.
4. Update parser to allow boolean literals.
5. Extend semantic analysis to enforce boolean usage.
6. Add new bytecode instruction `PUSH_BOOL`.
7. Update interpreter to evaluate boolean literals.
8. Add tests for lexer, parser, semantic analysis, codegen, and interpreter.

## Recommended testing strategy

- Start with unit tests for the lexer and parser.
- Add semantic tests for error cases.
- Add codegen tests that validate instruction sequences.
- Update smoke tests only when necessary to keep CI stable.
