from __future__ import annotations
from typing import Any, Dict


class Neo4jGraph:
    def __init__(self, uri: str | None = None, user: str | None = None, password: str | None = None) -> None:
        self.uri = uri
        self.user = user
        self.password = password
        self.nodes = {}

    def add_node(self, id: str, label: str, properties: Dict[str, Any] | None = None) -> None:
        self.nodes[id] = {"label": label, "properties": properties or {}}

    def query(self, query: str):
        return []
