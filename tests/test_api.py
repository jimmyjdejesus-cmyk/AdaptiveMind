"""Tests for FastAPI endpoints using the lightweight test harness."""

from pathlib import Path
import sys

from fastapi.testclient import TestClient

# Ensure the repository root is on the import path so ``app`` can be imported
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.test_harness import create_test_app


class FakeGraph:
    """Simple stand-in for ``Neo4jGraph`` used in tests."""

    def __init__(self, history=None, alive=True):
        self._history = history
        self._alive = alive

    def get_mission_history(self, mission_id: str):
        if mission_id == "bad":
            raise ValueError("invalid id")
        return self._history

    def is_alive(self) -> bool:
        return self._alive


def test_mission_history_success():
    """Mission history returns data when available."""
    fake = FakeGraph({"id": "123", "steps": [], "facts": []})
    app = create_test_app(fake)
    client = TestClient(app)

    resp = client.get("/missions/123/history")
    assert resp.status_code == 200
    assert resp.json() == {"id": "123", "steps": [], "facts": []}


def test_mission_history_not_found():
    """Endpoint responds with 404 when mission is missing."""
    fake = FakeGraph(None)
    app = create_test_app(fake)
    client = TestClient(app)

    resp = client.get("/missions/123/history")
    assert resp.status_code == 404


def test_mission_history_invalid_id():
    """Endpoint returns 400 for invalid IDs from graph layer."""
    fake = FakeGraph()
    app = create_test_app(fake)
    client = TestClient(app)

    resp = client.get("/missions/bad/history")
    assert resp.status_code == 400


def test_health_endpoint():
    """Health endpoint reflects graph activity."""
    fake = FakeGraph(alive=False)
    app = create_test_app(fake)
    client = TestClient(app)

    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"neo4j_active": False}
