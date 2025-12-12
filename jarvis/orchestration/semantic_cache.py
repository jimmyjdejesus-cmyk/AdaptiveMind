from __future__ import annotations
from typing import Any, Dict


class SemanticCache:
    """A minimal in-memory semantic cache used during tests.
    Provides a get/set API for storing computed semantic entries.
    """
    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value
