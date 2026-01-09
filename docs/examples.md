# MiniLang Examples

This document provides example MiniLang programs and their expected results.

## Example 1: Quickstart

```
let x = 40;
    y = 2;
    z = x + y
in
  z * 2
```

Expected result: `84`

## Example 2: Basic arithmetic

```
let a = 10;
    b = 3;
    c = a * b
in
  c - 5
```

Expected result: `25`

## Example 3: Parentheses and precedence

```
let x = 1 + 2 * 3;
    y = (1 + 2) * 3
in
  y - x
```

Expected result: `3`

## Example 4: Multiple declarations

```
let base = 5;
    multiplier = 6;
    total = base * multiplier
in
  total + 1
```

Expected result: `31`

## Example 5: Integer division

```
let a = 20;
    b = 6;
    c = a / b
in
  c + 1
```

Expected result: `4`

## Example 6: Using intermediate variables

```
let width = 7;
    height = 9;
    area = width * height;
    perimeter = width * 2 + height * 2
in
  area + perimeter
```

Expected result: `91`

## Example 7: Constant folding manually

```
let x = 2;
    y = 3;
    z = x * y
in
  z * z
```

Expected result: `36`

## Example 8: Larger program

```
let base = 100;
    offset = 25;
    scale = 3;
    adjusted = base - offset;
    scaled = adjusted * scale
in
  scaled / 5
```

Expected result: `45`

## Example 9: Chained operations

```
let a = 1;
    b = 2;
    c = 3;
    d = 4
in
  a + b + c + d
```

Expected result: `10`

## Example 10: Nested parentheses

```
let x = 5;
    y = 2
in
  ((x + y) * (x - y)) + (x / y)
```

Expected result: `21`

Use these examples to validate the compiler output or to create additional
integration tests.
