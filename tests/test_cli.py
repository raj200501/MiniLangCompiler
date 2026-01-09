import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "quickstart.minilang"


def run_cli(args, env=None):
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, "-m", "minilang_compiler.cli", *args],
        cwd=ROOT,
        env=merged_env,
        capture_output=True,
        text=True,
        check=False,
    )


class CliTests(unittest.TestCase):
    def test_cli_compile_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_cli(
                ["compile", str(EXAMPLE)],
                env={"PYTHONPATH": "src", "MINILANG_STORAGE_DIR": tmp_dir},
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("Compilation successful", result.stdout)

            compiled = Path(tmp_dir) / "s3" / "minilang-compiler-artifacts" / "quickstart.mlc"
            self.assertTrue(compiled.exists())

    def test_cli_run_prints_result(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = run_cli(
                ["run", str(EXAMPLE)],
                env={"PYTHONPATH": "src", "MINILANG_STORAGE_DIR": tmp_dir},
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("Result: 84", result.stdout)


if __name__ == "__main__":
    unittest.main()
