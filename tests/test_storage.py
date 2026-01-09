import tempfile
import unittest
from pathlib import Path

from minilang_compiler.codegen import generate
from minilang_compiler.lexer import tokenize
from minilang_compiler.parser import parse
from minilang_compiler.storage import LocalStorage


class StorageTests(unittest.TestCase):
    def test_local_storage_writes_compiled_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            program = parse(tokenize("let x = 1 in x"))
            compiled = generate(program)

            storage = LocalStorage(tmp_path)
            result = storage.upload_compiled("bucket", "sample", compiled)

            self.assertTrue(result.compiled_path.exists())
            self.assertTrue(result.metadata_path.exists())
            self.assertIn("PUSH 1", result.compiled_path.read_text(encoding="utf-8"))

    def test_local_storage_logs_error(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            storage = LocalStorage(tmp_path)
            result = storage.log_error("table", "sample", "boom")
            self.assertIsNotNone(result.log_path)
            self.assertTrue(result.log_path.exists())
            self.assertIn("boom", result.log_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
