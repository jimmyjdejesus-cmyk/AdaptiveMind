"""Route curiosity questions into mission directive queue."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

try:  # pragma: no cover - optional redis dependency
    from jarvis.orchestration.task_queue import RedisTaskQueue
except Exception:  # pragma: no cover - fallback for tests without redis
    class RedisTaskQueue:  # type: ignore
        """Fallback in-memory queue used when Redis is unavailable."""

        def __init__(self, *args: any, **kwargs: any) -> None:  # pragma: no cover - test stub
            self.items: list[dict] = []

        def enqueue(self, task: dict) -> None:  # pragma: no cover - test stub
            self.items.append(task)


@dataclass
class CuriosityRouter:
    """Enqueue curiosity questions as new mission directives."""

    queue: RedisTaskQueue
    enabled: bool = True

    def __init__(self, queue: Optional[RedisTaskQueue] = None, enabled: bool = True) -> None:
        self.queue = queue or RedisTaskQueue(name="curiosity_directives")
        self.enabled = enabled

    def route(self, question: str) -> None:
        """Enqueue ``question`` as a mission directive if routing is enabled."""
        if not self.enabled:
            return
        task = {"type": "directive", "request": question}
        self.queue.enqueue(task)
