"""Replay memory for storing agent reasoning trajectories."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Deque, Iterable, List, Tuple
import random

from .memory_bus import MemoryBus

Transition = Tuple[Any, Any, float, Any, bool]


@dataclass
class ReplayMemory:
    """Simple replay buffer with optional logging via :class:`MemoryBus`."""
    capacity: int = 1000
    memory_bus: MemoryBus | None = None

    def __post_init__(self) -> None:
        self._memory: Deque[Transition] = deque(maxlen=self.capacity)
        if self.memory_bus is None:
            # Default to local memory bus in current directory
            self.memory_bus = MemoryBus()

    # -- core API ---------------------------------------------------------
    def push(self, state: Any, action: Any, reward: float, next_state: Any, done: bool) -> None:
        """Store a transition and log the interaction."""
        transition: Transition = (state, action, reward, next_state, done)
        self._memory.append(transition)
        if self.memory_bus:
            self.memory_bus.log_interaction(
                agent_id="replay_memory",
                team="system",
                message="push",
                data={
                    "state": state,
                    "action": action,
                    "reward": reward,
                    "next_state": next_state,
                    "done": done,
                },
            )

    def recall(self, state: Any, top_k: int = 1) -> List[Transition]:
        """Retrieve transitions with matching state and log the recall."""
        matches = [t for t in reversed(self._memory) if t[0] == state][:top_k]
        if self.memory_bus:
            for t in matches:
                self.memory_bus.log_interaction(
                    agent_id="replay_memory",
                    team="system",
                    message="recall",
                    data={
                        "state": t[0],
                        "action": t[1],
                        "reward": t[2],
                        "next_state": t[3],
                        "done": t[4],
                    },
                )
        return matches

    def sample(self, batch_size: int) -> List[Transition]:
        """Randomly sample a batch of transitions."""
        return random.sample(list(self._memory), batch_size)

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._memory)
