"""Generate stack-based bytecode for MiniLang."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .ast import BinOpExpr, Decl, Expr, IntLiteral, Program, Var


@dataclass(frozen=True)
class Instruction:
    opcode: str
    operand: str | None = None

    def render(self) -> str:
        if self.operand is None:
            return self.opcode
        return f"{self.opcode} {self.operand}"


@dataclass(frozen=True)
class CompiledProgram:
    instructions: List[Instruction]

    def render(self) -> str:
        return "\n".join(instr.render() for instr in self.instructions)


def generate(program: Program) -> CompiledProgram:
    instructions: List[Instruction] = []
    env: Dict[str, None] = {}
    for decl in program.decls:
        _emit_expr(decl.expr, instructions)
        instructions.append(Instruction("STORE", decl.name))
        env[decl.name] = None
    _emit_expr(program.body, instructions)
    instructions.append(Instruction("RETURN"))
    return CompiledProgram(instructions=instructions)


def _emit_expr(expr: Expr, instructions: List[Instruction]) -> None:
    if isinstance(expr, IntLiteral):
        instructions.append(Instruction("PUSH", str(expr.value)))
        return
    if isinstance(expr, Var):
        instructions.append(Instruction("LOAD", expr.name))
        return
    if isinstance(expr, BinOpExpr):
        _emit_expr(expr.left, instructions)
        _emit_expr(expr.right, instructions)
        opcode = {
            "+": "ADD",
            "-": "SUB",
            "*": "MUL",
            "/": "DIV",
        }[expr.op.value]
        instructions.append(Instruction(opcode))
        return
    raise ValueError(f"Unsupported expression: {expr}")


def interpret(program: Program) -> int:
    values: Dict[str, int] = {}
    for decl in program.decls:
        values[decl.name] = _eval_expr(decl.expr, values)
    return _eval_expr(program.body, values)


def _eval_expr(expr: Expr, values: Dict[str, int]) -> int:
    if isinstance(expr, IntLiteral):
        return expr.value
    if isinstance(expr, Var):
        return values[expr.name]
    if isinstance(expr, BinOpExpr):
        left = _eval_expr(expr.left, values)
        right = _eval_expr(expr.right, values)
        if expr.op.value == "+":
            return left + right
        if expr.op.value == "-":
            return left - right
        if expr.op.value == "*":
            return left * right
        if expr.op.value == "/":
            return left // right
    raise ValueError(f"Unsupported expression: {expr}")


def collect_symbols(program: Program) -> List[str]:
    symbols: List[str] = []
    for decl in program.decls:
        symbols.append(decl.name)
    return symbols
