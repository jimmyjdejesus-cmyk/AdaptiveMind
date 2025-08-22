import importlib
import sys
from pathlib import Path


def test_visualizer_indicators():
    sys.modules.pop("ui", None)
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    viz_mod = importlib.import_module("ui.visualizer")
    WorkflowVisualizer = viz_mod.WorkflowVisualizer

    events = [
        {"step": "A", "status": "active"},
        {"step": "B", "status": "pruned"},
        {"step": "C", "status": "active", "merged_from": ["B"], "depends": ["A"]},
    ]
    viz = WorkflowVisualizer(events)
    graph = viz._build_graph()
    dot = "\n".join(graph.body)
    assert "A" in dot and "color=green" in dot
    assert "B" in dot and "color=red" in dot
    assert "B -> C" in dot and "style=dashed" in dot
