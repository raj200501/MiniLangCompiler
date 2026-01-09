import unittest

from minilang_compiler.lexer import tokenize
from minilang_compiler.parser import parse
from minilang_compiler.semant import SemanticError, analyze, collect_warnings


class SemantTests(unittest.TestCase):
    def test_semantic_checks_unbound_var(self):
        program = parse(tokenize("let x = 1 in y"))
        with self.assertRaises(SemanticError):
            analyze(program)

    def test_semantic_checks_duplicate_decl(self):
        program = parse(tokenize("let x = 1; x = 2 in x"))
        with self.assertRaises(SemanticError):
            analyze(program)

    def test_semantic_allows_ordered_decl(self):
        program = parse(tokenize("let x = 1; y = x + 2 in y"))
        analyze(program)

    def test_semantic_detects_division_by_literal_zero(self):
        program = parse(tokenize("let x = 10 / 0 in x"))
        with self.assertRaises(SemanticError):
            analyze(program)

    def test_collect_warnings_unused_variable(self):
        program = parse(tokenize("let x = 1; y = 2 in x"))
        analyze(program)
        warnings = collect_warnings(program)
        self.assertTrue(any("Unused variable 'y'" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main()
