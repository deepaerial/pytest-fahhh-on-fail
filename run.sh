#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
    echo "uv not found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

if ! command -v uv >/dev/null 2>&1; then
    echo "uv was installed but could not be found on PATH" >&2
    echo "add uv to your PATH and re-run this script" >&2
    exit 1
fi

uv sync
uv run pytest test_fail.py
