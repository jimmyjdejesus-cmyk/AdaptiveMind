"""Basic API-related tests focusing on memory interactions."""

from jarvis.memory.memory_bus import MemoryBus
from jarvis.memory.replay_memory import ReplayMemory


def test_push_and_recall(tmp_path) -> None:
    bus = MemoryBus(tmp_path)
    memory = ReplayMemory(capacity=10, log_dir=bus.log_file.parent)
    memory.push("s1", "a1", 1.0, "s2", False)
    memory.push("s1", "a2", 0.5, "s3", True)
    recalled = memory.recall("s1", top_k=2)
    assert len(recalled) == 2
    assert recalled[0].action == "a2"
    assert recalled[1].action == "a1"
    log_content = bus.read_log()
    assert "push" in log_content
    assert "recall" in log_content

