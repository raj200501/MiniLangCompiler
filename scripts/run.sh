#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <source-file> [compile|run|check]"
  exit 1
fi

SOURCE="$1"
COMMAND="${2:-compile}"
PYTHONPATH=src python -m minilang_compiler.cli "$COMMAND" "$SOURCE"
