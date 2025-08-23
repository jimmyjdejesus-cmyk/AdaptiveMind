import os
import sys

sys.path.append(os.getcwd())

from jarvis.learning import PolicyOptimizer
from jarvis.world_model.hypergraph import HierarchicalHypergraph


def test_policy_optimizer_updates_strategy():
    hg = HierarchicalHypergraph()
    key = hg.add_strategy(["step"], confidence=0.2)
    opt = PolicyOptimizer(hg, learning_rate=0.5)
    opt.update_strategy(key, reward=1.0)
    node = hg.query(2, key)
    assert node is not None
    assert node["confidence"] > 0.2
