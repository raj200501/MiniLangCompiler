"""AST definitions and source locations for MiniLang."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass(frozen=True)
class SourceLocation:
    line: int
    column: int

    def __str__(self) -> str:
        return f"line {self.line}, column {self.column}"


class TokenKind(str, Enum):
    LET = "LET"
    IN = "IN"
    IDENT = "IDENT"
    INT = "INT"
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIV = "/"
    EQ = "="
    LPAREN = "("
    RPAREN = ")"
    SEMI = ";"
    EOF = "EOF"


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    value: Optional[str]
    location: SourceLocation

    def __str__(self) -> str:
        if self.value is None:
            return f"{self.kind} at {self.location}"
        return f"{self.kind}({self.value}) at {self.location}"


class BinOp(str, Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"


class Expr:
    location: SourceLocation

    def pretty(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class IntLiteral(Expr):
    value: int
    location: SourceLocation

    def pretty(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Var(Expr):
    name: str
    location: SourceLocation

    def pretty(self) -> str:
        return self.name


@dataclass(frozen=True)
class BinOpExpr(Expr):
    left: Expr
    op: BinOp
    right: Expr
    location: SourceLocation

    def pretty(self) -> str:
        return f"({self.left.pretty()} {self.op.value} {self.right.pretty()})"


@dataclass(frozen=True)
class Decl:
    name: str
    expr: Expr
    location: SourceLocation


@dataclass(frozen=True)
class Program:
    decls: List[Decl]
    body: Expr

    def pretty(self) -> str:
        decls = "\n".join(f"let {decl.name} = {decl.expr.pretty()}" for decl in self.decls)
        return f"{decls}\n--\n{self.body.pretty()}"
