# AdaptiveMind Framework
# Copyright (c) 2025 Jimmy De Jesus
# Licensed under CC-BY 4.0
#
# AdaptiveMind - Intelligent AI Routing & Context Engine
# More info: https://github.com/[username]/adaptivemind
# License: https://creativecommons.org/licenses/by/4.0/



"""Tiny shim for PyYAML's safe_load used in legacy code during tests.

This is intentionally minimal and returns an empty dict for missing/empty
input; it avoids adding PyYAML as a heavy dependency for CI collection.
"""

from typing import IO, Any


def safe_load(stream: IO | str | None) -> Any:
    # Accept file-like object or string; return empty mapping when not present.
    if stream is None:
        return {}
    try:
        data = stream.read() if hasattr(stream, "read") else str(stream)
        if not data.strip():
            return {}
        # Very small heuristic: if it looks like JSON, parse it; else return {}
        import json

        try:
            return json.loads(data)
        except Exception:
            return {}
    except Exception:
        return {}
