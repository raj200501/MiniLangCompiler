import unittest

from minilang_compiler.ast import TokenKind
from minilang_compiler.lexer import LexerError, tokenize


def token_kinds(source: str):
    return [token.kind for token in tokenize(source)]


class LexerTests(unittest.TestCase):
    def test_tokenizes_basic_program(self):
        kinds = token_kinds("let x = 1 in x")
        self.assertEqual(
            kinds,
            [
                TokenKind.LET,
                TokenKind.IDENT,
                TokenKind.EQ,
                TokenKind.INT,
                TokenKind.IN,
                TokenKind.IDENT,
                TokenKind.EOF,
            ],
        )

    def test_tokenizes_operators_and_parentheses(self):
        kinds = token_kinds("let x = (1 + 2) * 3 in x")
        self.assertIn(TokenKind.LPAREN, kinds)
        self.assertIn(TokenKind.RPAREN, kinds)
        self.assertIn(TokenKind.PLUS, kinds)
        self.assertIn(TokenKind.TIMES, kinds)

    def test_tokenizes_semicolons(self):
        kinds = token_kinds("let x = 1; y = 2 in x + y")
        self.assertIn(TokenKind.SEMI, kinds)

    def test_tokenizes_comments(self):
        kinds = token_kinds("# comment\nlet x = 1 // trailing\nin x")
        self.assertIn(TokenKind.LET, kinds)
        self.assertIn(TokenKind.IN, kinds)

    def test_lexer_error_on_invalid_character(self):
        with self.assertRaises(LexerError):
            list(tokenize("let x = 1 in @"))


if __name__ == "__main__":
    unittest.main()
