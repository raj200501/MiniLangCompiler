# MiniLang Language Guide

This document is the authoritative description of the MiniLang DSL implemented by the
Python compiler in `src/minilang_compiler/`.

## Overview

MiniLang is intentionally small and deterministic. It was designed for compiler
exercises and automated build verification. A program consists of a `let` block
that declares one or more integer bindings, followed by an `in` expression that
produces the program result.

MiniLang has no I/O, no mutable state, and no side effects. Every program evaluates
to an integer, which means the compiler can safely emit stack-based bytecode or
interpret directly.

## Syntax summary

```
program  := "let" decls "in" expr

decls    := decl (";" decl)*

decl     := IDENT "=" expr

expr     := term (("+" | "-") term)*
term     := factor (("*" | "/") factor)*

factor   := INT | IDENT | "(" expr ")"
```

### Tokens

- `let`, `in` are reserved keywords.
- `IDENT` is an identifier matching `[A-Za-z_][A-Za-z0-9_]*`.
- `INT` is a base-10 integer literal.
- Comments start with `#` or `//` and continue to the end of the line.

### Whitespace

Whitespace is ignored everywhere. Newlines do not terminate declarations, so
use semicolons when you want to include multiple declarations in a single `let`
block. Example:

```
let x = 1;
    y = x + 2
in
  y * 3
```

## Expressions

MiniLang expressions always produce an integer. The following operators are
supported:

- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Integer division (`/`)

Operator precedence matches conventional arithmetic:

1. `*` and `/` (left associative)
2. `+` and `-` (left associative)

Parentheses can be used to override precedence.

### Examples

```
let x = 8;
    y = (x + 2) * 3
in
  y - 4
```

```
let a = 10;
    b = 5
in
  (a / b) + (a * b)
```

## Declarations

Declarations are ordered. Each declaration can refer to any name declared before
it. Attempting to reference a variable that is not yet declared is a semantic
error.

Valid:

```
let x = 1;
    y = x + 2
in
  y * 5
```

Invalid (unbound `y`):

```
let x = y + 2;
    y = 1
in
  x
```

## Semantics

The compiler performs a semantic check after parsing:

- Duplicate declarations are rejected.
- Unbound variables are rejected.
- Division by a literal zero is rejected.
- Unused variables are reported as warnings.

The semantic check runs in `minilang_compiler.semant.analyze`.

## Bytecode output

Compiled programs are represented as stack-based bytecode instructions. The
`minilang_compiler.codegen` module emits these instructions. Each declaration
emits a `STORE` to a named slot. Expressions push values onto the stack and
consume them with operators. The final expression result is left on the stack
and terminated with `RETURN`.

Example program:

```
let x = 1;
    y = x + 2
in
  y * 3
```

Compiled output:

```
PUSH 1
STORE x
LOAD x
PUSH 2
ADD
STORE y
LOAD y
PUSH 3
MUL
RETURN
```

## Interpreting MiniLang

The compiler also includes an interpreter used by the `run` command. The
interpreter evaluates the AST directly and returns the integer result. It uses
the same semantics as the compiler, which allows the test suite to compare
results without executing bytecode.

## Error messages

Errors include line and column information, so that compilation failures can be
traced to a precise location in the input. Example error message:

```
SemanticError: Unbound variable 'x' at line 4, column 3
```

## Style guide

To keep MiniLang programs readable and aligned with the documentation, follow
these conventions:

- Use one declaration per line.
- Indent the declarations in the `let` block by two spaces or more.
- Use parentheses around mixed operators if the intent is not obvious.

Example:

```
let base = 40;
    increment = 2;
    total = base + increment
in
  total * 2
```

## Future extensions

MiniLang intentionally remains minimal, but the compiler has been structured to
support extensions. Suggested additions include:

- Boolean literals and comparison operators
- Conditional expressions (e.g., `if ... then ... else ...`)
- Let blocks with nested scopes
- Functions and function calls
- String literals

If you implement an extension, update this language guide and the corresponding
compiler modules.
