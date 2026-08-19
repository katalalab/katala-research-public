#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required; install uv and rerun scripts/verify.sh" >&2
  exit 127
fi

uv run --locked --extra dev pytest -q "$@"
