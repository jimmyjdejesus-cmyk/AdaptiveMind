import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.append(str(root / "jarvis"))

from memory.memory_bus import MemoryBus
from memory.replay_memory import ReplayMemory


def test_push_and_recall(tmp_path):
    bus = MemoryBus(tmp_path)
    memory = ReplayMemory(capacity=10, memory_bus=bus)
    memory.push("s1", "a1", 1.0, "s2", False)
    memory.push("s1", "a2", 0.5, "s3", True)
    recalled = memory.recall("s1", top_k=2)
    assert len(recalled) == 2
    assert recalled[0][1] == "a2"
    assert recalled[1][1] == "a1"
    log_content = bus.read_log()
    assert "push" in log_content
    assert "recall" in log_content
