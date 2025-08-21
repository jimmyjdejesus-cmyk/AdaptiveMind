"""Memory management utilities for Jarvis AI."""

from __future__ import annotations

# Importing project memory can fail in minimal environments where optional
# dependencies like Chroma are unavailable. Perform the import lazily so that
# basic utilities (e.g. MemoryClient) remain usable.
try:  # pragma: no cover - optional import
    from .project_memory import MemoryManager, ProjectMemory  # type: ignore

    __all__ = ["MemoryManager", "ProjectMemory"]
except Exception:  # pragma: no cover - import guard
    __all__: list[str] = []
