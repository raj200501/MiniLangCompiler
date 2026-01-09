"""Command line interface for MiniLangCompiler."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from .compiler import CompileFailure, check_file, compile_and_run, compile_file
from .config import Config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="minilangc",
        description="Compile MiniLang source files and store compiled artifacts.",
    )
    parser.add_argument("--config", type=Path, help="Path to config JSON (default: config/minilang.json)")
    subparsers = parser.add_subparsers(dest="command", required=False)

    compile_parser = subparsers.add_parser("compile", help="Compile a MiniLang source file")
    compile_parser.add_argument("source", type=Path, help="Path to a .minilang source file")

    run_parser = subparsers.add_parser("run", help="Compile and run a MiniLang source file")
    run_parser.add_argument("source", type=Path, help="Path to a .minilang source file")

    check_parser = subparsers.add_parser("check", help="Parse and type-check a source file")
    check_parser.add_argument("source", type=Path, help="Path to a .minilang source file")

    return parser


def _emit_warnings(warnings: List[str]) -> None:
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = Config.load(args.config)
    command = args.command or "compile"

    try:
        if command == "compile":
            result = compile_file(args.source, config)
            _emit_warnings(result.warnings)
            print("Compilation successful.")
            print(f"Compiled output: {result.storage_result.compiled_path}")
            print(f"Metadata: {result.storage_result.metadata_path}")
            return 0
        if command == "run":
            result = compile_and_run(args.source, config)
            _emit_warnings(result.warnings)
            print("Compilation successful.")
            print(f"Result: {result.result_value}")
            print(f"Compiled output: {result.storage_result.compiled_path}")
            return 0
        if command == "check":
            result = check_file(args.source)
            _emit_warnings(result.warnings)
            print("Check successful.")
            print(f"Symbols: {', '.join(sorted({d.name for d in result.program.decls}))}")
            return 0
    except CompileFailure as exc:
        print(f"Compilation failed: {exc}")
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
