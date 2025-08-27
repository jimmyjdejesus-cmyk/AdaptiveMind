"""Test configuration to ensure package imports."""

import sys
from pathlib import Path
from unittest.mock import MagicMock
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def mock_neo4j_graph(monkeypatch):
    """Provide a mock Neo4j graph for tests.

    This fixture patches both the Neo4jGraph class used by core modules and the
    instantiated ``neo4j_graph`` in ``app.main`` so tests can run without a
    real database connection.
    """

    mock_graph = MagicMock()

    try:
        import jarvis.world_model.neo4j_graph as neo_module
        monkeypatch.setattr(neo_module, "Neo4jGraph", MagicMock(return_value=mock_graph))
    except Exception:
        pass

    try:
        import app.main as main_app
        monkeypatch.setattr(main_app, "neo4j_graph", mock_graph)
    except Exception:
        pass

    return mock_graph
