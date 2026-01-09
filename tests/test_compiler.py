import tempfile
import unittest
from pathlib import Path

from minilang_compiler.compiler import CompileFailure, compile_file
from minilang_compiler.config import Config


class CompilerTests(unittest.TestCase):
    def test_compile_file_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            source = tmp_path / "sample.minilang"
            source.write_text("let x = 1 in x", encoding="utf-8")
            config = Config(bucket="bucket", table="table", storage_dir=tmp_path, aws_mode=False)

            result = compile_file(source, config)

            self.assertTrue(result.storage_result.compiled_path.exists())
            self.assertTrue(result.storage_result.metadata_path.exists())

    def test_compile_file_logs_error(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            source = tmp_path / "bad.minilang"
            source.write_text("let x = 1 in y", encoding="utf-8")
            config = Config(bucket="bucket", table="table", storage_dir=tmp_path, aws_mode=False)

            with self.assertRaises(CompileFailure):
                compile_file(source, config)

            log_path = tmp_path / "dynamodb" / "table.jsonl"
            self.assertTrue(log_path.exists())
            self.assertIn("Unbound variable", log_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
