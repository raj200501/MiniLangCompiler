"""Recursive descent parser for MiniLang."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .ast import BinOp, BinOpExpr, Decl, Expr, IntLiteral, Program, SourceLocation, Token, TokenKind, Var


@dataclass(frozen=True)
class ParserError(Exception):
    message: str
    location: SourceLocation

    def __str__(self) -> str:
        return f"ParserError: {self.message} at {self.location}"


class Parser:
    def __init__(self, tokens: Iterable[Token]) -> None:
        self.tokens = list(tokens)
        self.index = 0

    def _peek(self) -> Token:
        return self.tokens[self.index]

    def _advance(self) -> Token:
        token = self._peek()
        if token.kind != TokenKind.EOF:
            self.index += 1
        return token

    def _expect(self, kind: TokenKind) -> Token:
        token = self._peek()
        if token.kind != kind:
            raise ParserError(f"Expected {kind} but found {token.kind}", token.location)
        return self._advance()

    def parse(self) -> Program:
        if self._peek().kind != TokenKind.LET:
            token = self._peek()
            raise ParserError("Program must start with 'let'", token.location)
        self._advance()
        decls = self._parse_decls()
        self._expect(TokenKind.IN)
        body = self._parse_expr()
        if self._peek().kind != TokenKind.EOF:
            token = self._peek()
            raise ParserError("Unexpected tokens after program", token.location)
        return Program(decls=decls, body=body)

    def _parse_decls(self) -> List[Decl]:
        decls = [self._parse_decl()]
        while self._peek().kind == TokenKind.SEMI:
            self._advance()
            if self._peek().kind == TokenKind.IN:
                break
            decls.append(self._parse_decl())
        return decls

    def _parse_decl(self) -> Decl:
        ident = self._expect(TokenKind.IDENT)
        self._expect(TokenKind.EQ)
        expr = self._parse_expr()
        return Decl(name=ident.value or "", expr=expr, location=ident.location)

    def _parse_expr(self) -> Expr:
        expr = self._parse_term()
        while self._peek().kind in {TokenKind.PLUS, TokenKind.MINUS}:
            token = self._advance()
            right = self._parse_term()
            op = BinOp.ADD if token.kind == TokenKind.PLUS else BinOp.SUB
            expr = BinOpExpr(left=expr, op=op, right=right, location=token.location)
        return expr

    def _parse_term(self) -> Expr:
        expr = self._parse_factor()
        while self._peek().kind in {TokenKind.TIMES, TokenKind.DIV}:
            token = self._advance()
            right = self._parse_factor()
            op = BinOp.MUL if token.kind == TokenKind.TIMES else BinOp.DIV
            expr = BinOpExpr(left=expr, op=op, right=right, location=token.location)
        return expr

    def _parse_factor(self) -> Expr:
        token = self._peek()
        if token.kind == TokenKind.INT:
            self._advance()
            return IntLiteral(value=int(token.value or "0"), location=token.location)
        if token.kind == TokenKind.IDENT:
            self._advance()
            return Var(name=token.value or "", location=token.location)
        if token.kind == TokenKind.LPAREN:
            self._advance()
            expr = self._parse_expr()
            self._expect(TokenKind.RPAREN)
            return expr
        raise ParserError("Expected expression", token.location)


def parse(tokens: Iterable[Token]) -> Program:
    return Parser(tokens).parse()
