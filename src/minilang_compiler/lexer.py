"""Tokenize MiniLang source text."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .ast import SourceLocation, Token, TokenKind


@dataclass(frozen=True)
class LexerError(Exception):
    message: str
    location: SourceLocation

    def __str__(self) -> str:
        return f"LexerError: {self.message} at {self.location}"


KEYWORDS = {
    "let": TokenKind.LET,
    "in": TokenKind.IN,
}

SINGLE_CHAR_TOKENS = {
    "+": TokenKind.PLUS,
    "-": TokenKind.MINUS,
    "*": TokenKind.TIMES,
    "/": TokenKind.DIV,
    "=": TokenKind.EQ,
    "(": TokenKind.LPAREN,
    ")": TokenKind.RPAREN,
    ";": TokenKind.SEMI,
}


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.index = 0
        self.line = 1
        self.column = 1

    def _peek(self) -> str:
        if self.index >= len(self.source):
            return ""
        return self.source[self.index]

    def _advance(self) -> str:
        ch = self._peek()
        self.index += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _location(self) -> SourceLocation:
        return SourceLocation(self.line, self.column)

    def _skip_whitespace(self) -> None:
        while True:
            ch = self._peek()
            if ch == "" or not ch.isspace():
                break
            self._advance()

    def _skip_comment(self) -> bool:
        if self._peek() == "#":
            while self._peek() not in {"", "\n"}:
                self._advance()
            return True
        if self._peek() == "/" and self.index + 1 < len(self.source) and self.source[self.index + 1] == "/":
            while self._peek() not in {"", "\n"}:
                self._advance()
            return True
        return False

    def tokens(self) -> Iterable[Token]:
        while True:
            self._skip_whitespace()
            if self._skip_comment():
                continue

            location = self._location()
            ch = self._peek()
            if ch == "":
                yield Token(TokenKind.EOF, None, location)
                return

            if ch in SINGLE_CHAR_TOKENS:
                self._advance()
                yield Token(SINGLE_CHAR_TOKENS[ch], ch, location)
                continue

            if ch.isdigit():
                value = self._consume_number()
                yield Token(TokenKind.INT, value, location)
                continue

            if ch.isalpha() or ch == "_":
                value = self._consume_identifier()
                kind = KEYWORDS.get(value, TokenKind.IDENT)
                yield Token(kind, value, location)
                continue

            raise LexerError(f"Unexpected character '{ch}'", location)

    def _consume_number(self) -> str:
        digits: List[str] = []
        while self._peek().isdigit():
            digits.append(self._advance())
        return "".join(digits)

    def _consume_identifier(self) -> str:
        chars: List[str] = []
        while True:
            ch = self._peek()
            if not (ch.isalnum() or ch == "_"):
                break
            chars.append(self._advance())
        return "".join(chars)


def tokenize(source: str) -> List[Token]:
    return list(Lexer(source).tokens())
