#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

PYTHONPATH=src python -m unittest discover -s tests -p "test_*.py"

PYTHONPATH=src python scripts/smoke_test.py
