import unittest

from minilang_compiler.ast import BinOp, BinOpExpr, IntLiteral, Var
from minilang_compiler.lexer import tokenize
from minilang_compiler.parser import ParserError, parse


class ParserTests(unittest.TestCase):
    def test_parse_simple_program(self):
        program = parse(tokenize("let x = 1 in x"))
        self.assertEqual(len(program.decls), 1)
        self.assertEqual(program.decls[0].name, "x")
        self.assertIsInstance(program.body, Var)

    def test_parse_binary_expression(self):
        program = parse(tokenize("let x = 1 + 2 in x * 3"))
        self.assertIsInstance(program.decls[0].expr, BinOpExpr)
        self.assertEqual(program.decls[0].expr.op, BinOp.ADD)
        self.assertIsInstance(program.body, BinOpExpr)

    def test_parse_parentheses_affect_precedence(self):
        program = parse(tokenize("let x = (1 + 2) * 3 in x"))
        expr = program.decls[0].expr
        self.assertIsInstance(expr, BinOpExpr)
        self.assertEqual(expr.op, BinOp.MUL)

    def test_parse_multiple_decls(self):
        program = parse(tokenize("let x = 1; y = x + 2 in y"))
        self.assertEqual([decl.name for decl in program.decls], ["x", "y"])

    def test_parse_requires_let(self):
        with self.assertRaises(ParserError):
            parse(tokenize("x = 1"))

    def test_parse_rejects_trailing_tokens(self):
        with self.assertRaises(ParserError):
            parse(tokenize("let x = 1 in x 2"))

    def test_parse_number_literal(self):
        program = parse(tokenize("let x = 42 in x"))
        self.assertIsInstance(program.decls[0].expr, IntLiteral)


if __name__ == "__main__":
    unittest.main()
