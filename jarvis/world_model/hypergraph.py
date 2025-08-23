from __future__ import annotations

"""Simple hierarchical hypergraph for demo purposes.

This utility loads a three-layer dataset (concrete, abstract, causal) from a
JSON file and supports basic node lookup per layer. It is intentionally minimal
and only implements the features required by the Napoleon counterfactual demo.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import json


class HierarchicalHypergraph:
    """Load and query a multi-layer hypergraph dataset."""

    def __init__(self) -> None:
        self.layers: Dict[int, Dict[str, Dict[str, Any]]] = {1: {}, 2: {}, 3: {}}

    def load_from_json(self, path: str | Path) -> None:
        """Populate layers from a JSON file."""
        with open(Path(path), "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self.layers[1] = data.get("layer1_concrete", {})
        self.layers[2] = data.get("layer2_abstract", {})
        self.layers[3] = data.get("layer3_causal", {})

    def query(self, layer: int, node: str) -> Optional[Dict[str, Any]]:
        """Retrieve a node from a specific layer."""
        return self.layers.get(layer, {}).get(node)

    # ------------------------------------------------------------------
    def add_causal_belief(self, intervention: str, result: str, confidence: float) -> str:
        """Record a causal belief in Layer 3.

        Parameters
        ----------
        intervention:
            The intervention or action taken.
        result:
            The resulting outcome observed.
        confidence:
            Confidence score between 0 and 1.

        Returns
        -------
        str
            The key used to store the belief.
        """

        key = f"{intervention}->{result}"
        self.layers.setdefault(3, {})[key] = {
            "intervention": intervention,
            "result": result,
            "confidence": confidence,
        }
        return key

    def add_strategy(self, steps: List[str], confidence: float) -> str:
        """Create a strategy node in Layer 2 from reasoning steps."""
        key = f"strategy_{len(self.layers.get(2, {})) + 1}"
        self.layers.setdefault(2, {})[key] = {
            "steps": steps,
            "confidence": confidence,
        }
        return key

    def get_low_confidence_nodes(self, threshold: float) -> List[Tuple[int, str, Dict[str, Any]]]:
        """Return nodes across layers with confidence below ``threshold``."""
        low: List[Tuple[int, str, Dict[str, Any]]] = []
        for layer, nodes in self.layers.items():
            for key, data in nodes.items():
                if data.get("confidence", 1.0) < threshold:
                    low.append((layer, key, data))
        return low


__all__ = ["HierarchicalHypergraph"]
