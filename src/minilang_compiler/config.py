"""Configuration loader for MiniLangCompiler."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Config:
    bucket: str
    table: str
    storage_dir: Path
    aws_mode: bool

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        data: Dict[str, Any] = {}
        if config_path is None:
            default_path = Path("config/minilang.json")
            if default_path.exists():
                config_path = default_path
        if config_path is not None and config_path.exists():
            data = json.loads(config_path.read_text(encoding="utf-8"))

        bucket = os.getenv("MINILANG_BUCKET", data.get("bucket", "minilang-compiler-artifacts"))
        table = os.getenv("MINILANG_TABLE", data.get("table", "MiniLangCompilerLogs"))
        storage_dir = Path(os.getenv("MINILANG_STORAGE_DIR", data.get("storage_dir", "out")))
        aws_mode = os.getenv("MINILANG_AWS_MODE", str(data.get("aws_mode", "false"))).lower() in {
            "1",
            "true",
            "yes",
        }
        return cls(bucket=bucket, table=table, storage_dir=storage_dir, aws_mode=aws_mode)
