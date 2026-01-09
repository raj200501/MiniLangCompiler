"""Compiler pipeline for MiniLang."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from . import ast
from .codegen import CompiledProgram, generate, interpret
from .config import Config
from .lexer import LexerError, tokenize
from .parser import ParserError, parse
from .semant import SemanticError, analyze, collect_warnings
from .storage import StorageBackend, StorageResult, resolve_storage


@dataclass
class CompileResult:
    program: ast.Program
    compiled: CompiledProgram
    warnings: List[str]
    storage_result: StorageResult
    result_value: Optional[int] = None


@dataclass
class CheckResult:
    program: ast.Program
    warnings: List[str]


class CompileFailure(Exception):
    pass


def check_file(path: Path) -> CheckResult:
    if not path.exists():
        raise CompileFailure(f"Source file does not exist: {path}")

    source = path.read_text(encoding="utf-8")
    try:
        tokens = tokenize(source)
        program = parse(tokens)
        analyze(program)
        warnings = collect_warnings(program)
    except (LexerError, ParserError, SemanticError) as exc:
        raise CompileFailure(str(exc)) from exc

    return CheckResult(program=program, warnings=warnings)


def compile_file(path: Path, config: Config, storage: Optional[StorageBackend] = None) -> CompileResult:
    if not path.exists():
        raise CompileFailure(f"Source file does not exist: {path}")

    source = path.read_text(encoding="utf-8")
    try:
        tokens = tokenize(source)
        program = parse(tokens)
        analyze(program)
        warnings = collect_warnings(program)
        compiled = generate(program)
    except (LexerError, ParserError, SemanticError) as exc:
        storage_backend = storage or resolve_storage(config.storage_dir, config.aws_mode)
        storage_backend.log_error(config.table, path.name, str(exc))
        raise CompileFailure(str(exc)) from exc

    storage_backend = storage or resolve_storage(config.storage_dir, config.aws_mode)
    storage_result = storage_backend.upload_compiled(config.bucket, path.stem, compiled)
    return CompileResult(
        program=program,
        compiled=compiled,
        warnings=warnings,
        storage_result=storage_result,
    )


def compile_and_run(path: Path, config: Config) -> CompileResult:
    result = compile_file(path, config)
    result_value = interpret(result.program)
    return CompileResult(
        program=result.program,
        compiled=result.compiled,
        warnings=result.warnings,
        storage_result=result.storage_result,
        result_value=result_value,
    )
