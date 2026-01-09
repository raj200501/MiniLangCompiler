"""Smoke test for MiniLangCompiler CLI."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "quickstart.minilang"
OUT_DIR = ROOT / "out"


def main() -> int:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)

    env = os.environ.copy()
    env.update({
        "PYTHONPATH": "src",
        "MINILANG_STORAGE_DIR": str(OUT_DIR),
    })

    result = subprocess.run(
        [sys.executable, "-m", "minilang_compiler.cli", "run", str(EXAMPLE)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit("CLI run failed")

    compiled = OUT_DIR / "s3" / "minilang-compiler-artifacts" / "quickstart.mlc"
    metadata = OUT_DIR / "s3" / "minilang-compiler-artifacts" / "quickstart.json"
    if not compiled.exists():
        raise SystemExit("Compiled output missing")
    if not metadata.exists():
        raise SystemExit("Metadata output missing")

    metadata_data = json.loads(metadata.read_text(encoding="utf-8"))
    if metadata_data["key"] != "quickstart":
        raise SystemExit("Metadata key mismatch")
    if "RETURN" not in "\n".join(metadata_data["instructions"]):
        raise SystemExit("Compiled instructions missing RETURN")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
