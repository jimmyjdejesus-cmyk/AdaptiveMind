"""Pytest configuration with lightweight in-memory stubs."""
from __future__ import annotations

# flake8: noqa
from pathlib import Path
from unittest.mock import MagicMock
import sys
import types
import importlib.util
import enum
from dataclasses import dataclass
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Stub optional dependencies
sys.modules.setdefault("neo4j", MagicMock())


class RedisStub:
    """Minimal in-memory stand-in for ``redis.Redis``."""

    def __init__(self, *args, **kwargs) -> None:
        self._store: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        """Return the value stored at ``key`` or ``None`` if missing."""
        return self._store.get(key)

    def set(self, key: str, value: str) -> bool:
        """Store ``value`` at ``key`` and return ``True``."""
        self._store[key] = value
        return True

    def delete(self, *keys: str) -> int:
        """Remove ``keys`` from the store and return count removed."""
        removed = 0
        for k in keys:
            if k in self._store:
                del self._store[k]
                removed += 1
        return removed


redis_module = types.ModuleType("redis")
redis_module.Redis = RedisStub
sys.modules.setdefault("redis", redis_module)
keyring_errors = types.ModuleType("keyring.errors")


class NoKeyringError(Exception):
    """Placeholder for ``keyring.errors.NoKeyringError``."""

    pass


keyring_errors.NoKeyringError = NoKeyringError
keyring_module = types.ModuleType("keyring")
keyring_module.errors = keyring_errors
keyring_module.get_password = lambda *args, **kwargs: None
sys.modules.setdefault("keyring", keyring_module)
sys.modules.setdefault("keyring.errors", keyring_errors)

langgraph_graph = types.ModuleType("langgraph.graph")
langgraph_graph.END = object()


class StateGraph:  # pragma: no cover - minimal stub
    """Trivial stand-in for :class:`langgraph.graph.StateGraph`."""

    pass


langgraph_graph.StateGraph = StateGraph
langgraph_module = types.ModuleType("langgraph")
langgraph_module.graph = langgraph_graph
sys.modules.setdefault("langgraph", langgraph_module)
sys.modules.setdefault("langgraph.graph", langgraph_graph)
# In-memory qdrant_client implementation for tests


class Distance(enum.Enum):
    COSINE = "cosine"


@dataclass
class VectorParams:
    size: int
    distance: Distance


@dataclass
class MatchValue:
    value: str


@dataclass
class FieldCondition:
    key: str
    match: MatchValue


@dataclass
class Filter:
    must: list[FieldCondition]


@dataclass
class PointStruct:
    id: str
    vector: list[float]
    payload: dict


class InMemoryQdrantClient:
    """Minimal in-memory replacement for ``qdrant_client.QdrantClient``."""

    def __init__(self, url: str | None = None) -> None:
        self._collections: dict[str, dict[str, PointStruct]] = {}

    def collection_exists(self, collection_name: str) -> bool:
        """Return ``True`` if ``collection_name`` has been created."""
        return collection_name in self._collections

    def create_collection(
        self, collection_name: str, *, vectors_config: VectorParams
    ) -> None:  # pragma: no cover - trivial
        """Initialize an empty collection if it does not exist."""
        self._collections.setdefault(collection_name, {})

    def upsert(
        self,
        collection_name: str,
        points: list[PointStruct],
        wait: bool | None = None,
    ) -> None:
        """Insert or replace ``points`` within ``collection_name``."""
        coll = self._collections.setdefault(collection_name, {})
        for p in points:
            coll[p.id] = p

    def search(
        self,
        collection_name: str,
        query_vector: list[float],
        query_filter: Filter | None = None,
        limit: int = 10,
    ):
        """Return up to ``limit`` points ordered by simple L2 similarity."""
        coll = self._collections.get(collection_name, {})

        def similarity(p: PointStruct) -> float:
            return -sum((a - b) ** 2 for a, b in zip(p.vector, query_vector))

        return sorted(coll.values(), key=similarity, reverse=True)[:limit]

    def scroll(
        self,
        collection_name: str,
        scroll_filter: Filter | None = None,
        with_payload: bool = False,
        limit: int | None = None,
    ):
        """Iterate over ``collection_name`` applying ``scroll_filter`` if set."""
        coll = self._collections.get(collection_name, {})

        def matches(p: PointStruct) -> bool:
            if scroll_filter is None:
                return True
            return all(
                p.payload.get(cond.key) == cond.match.value
                for cond in scroll_filter.must
            )

        points = [p for p in coll.values() if matches(p)]
        return (points if limit is None else points[:limit], None)

    def delete(
        self,
        collection_name: str,
        *,
        points_selector: list[str] | None = None,
        filter: Filter | None = None,
        wait: bool | None = None,
    ) -> None:
        """Remove points by id or ``filter`` from ``collection_name``."""
        coll = self._collections.get(collection_name, {})
        if points_selector is not None:
            for pid in points_selector:
                coll.pop(pid, None)
        elif filter is not None:
            to_remove = [
                pid
                for pid, p in coll.items()
                if all(p.payload.get(c.key) == c.match.value for c in filter.must)
            ]
            for pid in to_remove:
                coll.pop(pid, None)


qdrant_client = types.ModuleType("qdrant_client")
qdrant_models = types.ModuleType("qdrant_client.models")
qdrant_client.QdrantClient = InMemoryQdrantClient
qdrant_models.Distance = Distance
qdrant_models.FieldCondition = FieldCondition
qdrant_models.Filter = Filter
qdrant_models.MatchValue = MatchValue
qdrant_models.PointStruct = PointStruct
qdrant_models.VectorParams = VectorParams
qdrant_client.models = qdrant_models
sys.modules.setdefault("qdrant_client", qdrant_client)
sys.modules.setdefault("qdrant_client.models", qdrant_models)
