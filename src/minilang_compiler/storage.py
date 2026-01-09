"""Storage backends for compiled code and logs."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .codegen import CompiledProgram


@dataclass
class StorageResult:
    compiled_path: Path
    metadata_path: Path
    log_path: Optional[Path] = None


class StorageError(Exception):
    pass


class StorageBackend:
    def upload_compiled(self, bucket: str, key: str, compiled: CompiledProgram) -> StorageResult:
        raise NotImplementedError

    def log_error(self, table: str, key: str, message: str) -> StorageResult:
        raise NotImplementedError


class LocalStorage(StorageBackend):
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def upload_compiled(self, bucket: str, key: str, compiled: CompiledProgram) -> StorageResult:
        bucket_dir = self.base_dir / "s3" / bucket
        bucket_dir.mkdir(parents=True, exist_ok=True)
        compiled_path = bucket_dir / f"{key}.mlc"
        metadata_path = bucket_dir / f"{key}.json"
        compiled_path.write_text(compiled.render() + "\n", encoding="utf-8")
        metadata = {
            "bucket": bucket,
            "key": key,
            "instructions": [instr.render() for instr in compiled.instructions],
        }
        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        return StorageResult(compiled_path=compiled_path, metadata_path=metadata_path)

    def log_error(self, table: str, key: str, message: str) -> StorageResult:
        table_dir = self.base_dir / "dynamodb"
        table_dir.mkdir(parents=True, exist_ok=True)
        log_path = table_dir / f"{table}.jsonl"
        entry = {
            "table": table,
            "key": key,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
        return StorageResult(compiled_path=log_path, metadata_path=log_path, log_path=log_path)


class AwsStorage(StorageBackend):
    def __init__(self) -> None:
        try:
            import boto3  # type: ignore
        except ImportError as exc:
            raise StorageError(
                "AWS mode requires boto3; install it or disable MINILANG_AWS_MODE"
            ) from exc
        self.session = boto3.session.Session()
        self.s3 = self.session.client("s3")
        self.dynamodb = self.session.client("dynamodb")

    def upload_compiled(self, bucket: str, key: str, compiled: CompiledProgram) -> StorageResult:
        body = compiled.render() + "\n"
        metadata = json.dumps({"key": key, "instructions": [instr.render() for instr in compiled.instructions]})
        self.s3.put_object(Bucket=bucket, Key=f"{key}.mlc", Body=body.encode("utf-8"))
        self.s3.put_object(Bucket=bucket, Key=f"{key}.json", Body=metadata.encode("utf-8"))
        placeholder = Path(f"s3://{bucket}/{key}")
        return StorageResult(compiled_path=placeholder, metadata_path=placeholder)

    def log_error(self, table: str, key: str, message: str) -> StorageResult:
        self.dynamodb.put_item(
            TableName=table,
            Item={
                "Key": {"S": key},
                "Message": {"S": message},
                "Timestamp": {"S": datetime.now(timezone.utc).isoformat()},
            },
        )
        placeholder = Path(f"dynamodb://{table}/{key}")
        return StorageResult(compiled_path=placeholder, metadata_path=placeholder, log_path=placeholder)


def resolve_storage(base_dir: Path, aws_mode: bool) -> StorageBackend:
    if aws_mode:
        return AwsStorage()
    return LocalStorage(base_dir)
