"""Core agent components with lightweight stubs for testing."""

from .core import AgentCore


class JarvisAgent:
    """Minimal agent used in tests for recall behavior."""

    def __init__(self, memory_bus):
        self.memory_bus = memory_bus

    def chat(self, message: str) -> str:
        self.memory_bus.log_interaction(
            "jarvis", "test", "push", {"msg": message}
        )
        return message

    def plan(self, message: str) -> str:
        self.memory_bus.log_interaction(
            "jarvis", "test", "recall", {"msg": message}
        )
        return message


__all__ = ["AgentCore", "JarvisAgent"]
