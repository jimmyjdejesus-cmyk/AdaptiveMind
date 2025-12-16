#!/usr/bin/env bash
set -euo pipefail

# Generate or refresh the project's uv.lock using uv
if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found; please install uv (e.g., brew install uv or use astral-sh/setup-uv in CI)"
  exit 1
fi

echo "Updating uv.lock"
uv lock --no-progress
echo "uv.lock updated"
