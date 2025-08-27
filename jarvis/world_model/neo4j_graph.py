"""Lightweight Neo4j adapter mirroring :class:`KnowledgeGraph` API."""

from __future__ import annotations

import os
import re
from typing import Any, Dict, Optional

from neo4j import GraphDatabase, Driver


class Neo4jGraph:
    """Persist graph entities to a Neo4j database."""

    def __init__(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        driver: Optional[Driver] = None,
    ) -> None:
        """Initialize a Neo4j driver.

        Parameters
        ----------
        uri, user, password:
            Optional overrides for connection information. If omitted, values
            fall back to ``NEO4J_URI``, ``NEO4J_USER`` and ``NEO4J_PASSWORD``
            environment variables.
        driver:
            Pre-configured :class:`neo4j.Driver` instance to reuse instead of
            creating a new connection.
        """

        if driver is not None:
            self.driver = driver
        else:
            uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
            user = user or os.getenv("NEO4J_USER", "neo4j")
            password = password or os.getenv("NEO4J_PASSWORD", "test")
            self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        """Close the underlying Neo4j driver."""

        self.driver.close()

    # ------------------------------------------------------------------
    def add_node(
        self, node_id: str, node_type: str, attributes: Optional[Dict[str, Any]] = None
    ) -> None:
        """Create or update a node in Neo4j.

        Parameters
        ----------
        node_id:
            Identifier for the node.
        node_type:
            Domain-specific node type label.
        attributes:
            Optional properties to store on the node.
        """

        props = attributes or {}
        with self.driver.session() as session:
            session.run(
                "MERGE (n:Node {id: $id}) SET n.type = $type, n += $props",
                id=node_id,
                type=node_type,
                props=props,
            )

    # ------------------------------------------------------------------
    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create or update an edge in Neo4j.

        Parameters
        ----------
        source_id:
            Identifier of the source node.
        target_id:
            Identifier of the target node.
        relationship_type:
            Type of relationship between ``source_id`` and ``target_id``.
        attributes:
            Optional edge properties.

        Raises
        ------
        ValueError
            If ``relationship_type`` does not match the allowed pattern.
        """

        props = attributes or {}
        rel = relationship_type.upper()
        if not re.fullmatch(r"[A-Z_][A-Z0-9_]*", rel):
            raise ValueError("Invalid relationship type")
        with self.driver.session() as session:
            session.run(
                f"MATCH (a:Node {{id: $source}}), (b:Node {{id: $target}}) "
                f"MERGE (a)-[r:{rel}]->(b) SET r += $props",
                source=source_id,
                target=target_id,
                props=props,
            )
