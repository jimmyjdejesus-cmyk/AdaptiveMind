from __future__ import annotations
from typing import Any, List


class PathMemory:
    """A simple path memory store used by the orchestrator during tests.

    The production PathMemory is more complex, but the tests only require
    adding decisions and possibly reading them back.
    """
    def __init__(self) -> None:
        self.decisions: List[Any] = []

    def add_decisions(self, decisions: List[Any]) -> None:
        if decisions:
            self.decisions.extend(decisions)

    def get_decisions(self) -> List[Any]:
        return list(self.decisions)
