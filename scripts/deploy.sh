#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <source-file>"
  echo "Requires MINILANG_AWS_MODE=true and AWS credentials in the environment."
  exit 1
fi

SOURCE="$1"

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

export MINILANG_AWS_MODE=true
PYTHONPATH=src python -m minilang_compiler.cli compile "$SOURCE"
