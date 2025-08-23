from __future__ import annotations

"""Simple REX-RAG policy optimizer."""

from typing import Dict, Any

from jarvis.world_model.hypergraph import HierarchicalHypergraph


class PolicyOptimizer:
    """Update strategy confidence based on reward feedback."""

    def __init__(self, hypergraph: HierarchicalHypergraph, learning_rate: float = 0.1) -> None:
        self.hypergraph = hypergraph
        self.learning_rate = learning_rate
        self.history: list[Dict[str, Any]] = []

    def update_strategy(self, strategy_key: str, reward: float) -> None:
        """Adjust the confidence of a strategy node using REX-RAG update rule."""
        node = self.hypergraph.query(2, strategy_key)
        if not node:
            return
        confidence = node.get("confidence", 0.5)
        updated = confidence + self.learning_rate * (reward - confidence)
        self.hypergraph.update_node(2, strategy_key, {"confidence": updated})
        self.history.append({"strategy": strategy_key, "reward": reward, "confidence": updated})
