from __future__ import annotations

"""Simple hierarchical hypergraph for demo purposes.

This utility loads a three-layer dataset (concrete, abstract, causal) from a
JSON file and supports basic node lookup per layer. It is intentionally minimal
and only implements the features required by the Napoleon counterfactual demo.
"""

from pathlib import Path
from typing import Dict, Any, Optional
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


__all__ = ["HierarchicalHypergraph"]
