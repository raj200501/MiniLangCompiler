"""Semantic analysis for MiniLang."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .ast import BinOpExpr, Decl, Expr, IntLiteral, Program, SourceLocation, Var


@dataclass(frozen=True)
class SemanticError(Exception):
    message: str
    location: SourceLocation

    def __str__(self) -> str:
        return f"SemanticError: {self.message} at {self.location}"


@dataclass(frozen=True)
class Symbol:
    name: str
    location: SourceLocation


def analyze(program: Program) -> Dict[str, Symbol]:
    env: Dict[str, Symbol] = {}
    for decl in program.decls:
        if decl.name in env:
            raise SemanticError(f"Duplicate declaration '{decl.name}'", decl.location)
        _check_expr(decl.expr, env)
        env[decl.name] = Symbol(name=decl.name, location=decl.location)
    _check_expr(program.body, env)
    return env


def _check_expr(expr: Expr, env: Dict[str, Symbol]) -> None:
    if isinstance(expr, IntLiteral):
        return
    if isinstance(expr, Var):
        if expr.name not in env:
            raise SemanticError(f"Unbound variable '{expr.name}'", expr.location)
        return
    if isinstance(expr, BinOpExpr):
        _check_expr(expr.left, env)
        _check_expr(expr.right, env)
        if expr.op.name == "DIV" and isinstance(expr.right, IntLiteral) and expr.right.value == 0:
            raise SemanticError("Division by literal zero", expr.location)
        return
    raise SemanticError("Unknown expression", getattr(expr, "location", SourceLocation(0, 0)))


def collect_warnings(program: Program) -> List[str]:
    used: Dict[str, bool] = {}
    for decl in program.decls:
        used[decl.name] = False
    _mark_used(program.body, used)
    warnings: List[str] = []
    for decl in program.decls:
        if not used.get(decl.name, False):
            warnings.append(f"Unused variable '{decl.name}' declared at {decl.location}")
    return warnings


def _mark_used(expr: Expr, used: Dict[str, bool]) -> None:
    if isinstance(expr, Var):
        if expr.name in used:
            used[expr.name] = True
        return
    if isinstance(expr, BinOpExpr):
        _mark_used(expr.left, used)
        _mark_used(expr.right, used)
        return
