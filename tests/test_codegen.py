import unittest

from minilang_compiler.codegen import CompiledProgram, generate, interpret
from minilang_compiler.lexer import tokenize
from minilang_compiler.parser import parse


class CodegenTests(unittest.TestCase):
    def test_codegen_emits_store_and_return(self):
        program = parse(tokenize("let x = 1 in x"))
        compiled = generate(program)
        rendered = compiled.render()
        self.assertIn("STORE x", rendered)
        self.assertTrue(rendered.strip().endswith("RETURN"))

    def test_interpret_matches_expected_value(self):
        program = parse(tokenize("let x = 2; y = x + 3 in y * 2"))
        self.assertEqual(interpret(program), 10)

    def test_codegen_compiled_program_render(self):
        program = parse(tokenize("let x = 1 in x + 2"))
        compiled = generate(program)
        self.assertIsInstance(compiled, CompiledProgram)
        self.assertTrue(any(instr.opcode == "ADD" for instr in compiled.instructions))


if __name__ == "__main__":
    unittest.main()
