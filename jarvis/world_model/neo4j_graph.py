"""Lightweight Neo4j adapter mirroring :class:`KnowledgeGraph` API."""

from __future__ import annotations

import os
import re
from typing import Any, Dict, Optional, List

from neo4j import GraphDatabase, Driver


class Neo4jGraph:
    """Persist graph entities to a Neo4j database."""

    SENSITIVE_FIELDS = {"password", "secret", "token"}

    def __init__(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        driver: Optional[Driver] = None,
    ) -> None:
        if driver is not None:
            self.driver = driver
        else:
            uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
            user = user or os.getenv("NEO4J_USER", "neo4j")
            password = password or os.getenv("NEO4J_PASSWORD", "test")
            self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        self.driver.close()

    # ------------------------------------------------------------------
    def add_node(self, node_id: str, node_type: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Create or update a node in Neo4j."""

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
        """Create or update an edge in Neo4j."""

        props = attributes or {}
        rel = relationship_type.upper()
        with self.driver.session() as session:
            session.run(
                f"MATCH (a:Node {{id: $source}}), (b:Node {{id: $target}}) "
                f"MERGE (a)-[r:{rel}]->(b) SET r += $props",
                source=source_id,
                target=target_id,
                props=props,
            )

    # ------------------------------------------------------------------
    def _sanitize_properties(self, props: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive fields from a properties dictionary."""

        return {k: v for k, v in props.items() if k.lower() not in self.SENSITIVE_FIELDS}

    # ------------------------------------------------------------------
    def get_mission_history(self, mission_id: str) -> Dict[str, Any]:
        """Fetch a mission with its steps and discovered facts.

        Args:
            mission_id: The ID of the mission to retrieve.

        Returns:
            A dictionary containing mission properties and lists of related steps
            and facts. Sensitive fields are removed. If the mission is not
            found, an empty dictionary is returned.
        """

        if not re.fullmatch(r"[\w-]+", mission_id):
            raise ValueError("Invalid mission_id")

        with self.driver.session() as session:
            result = session.run(
                (
                    "MATCH (m:Mission {id: $mission_id}) "
                    "OPTIONAL MATCH (m)-[:HAS_STEP]->(s:Step) "
                    "OPTIONAL MATCH (s)-[:DISCOVERED]->(f:Fact) "
                    "RETURN m, collect(DISTINCT s) AS steps, "
                    "collect(DISTINCT f) AS facts"
                ),
                mission_id=mission_id,
            )
            record = result.single()
            if not record:
                return {}

            mission = self._sanitize_properties(dict(record["m"]))
            steps = [self._sanitize_properties(dict(step)) for step in record["steps"] if step]
            facts = [self._sanitize_properties(dict(fact)) for fact in record["facts"] if fact]

            return {"mission": mission, "steps": steps, "facts": facts}

    # ------------------------------------------------------------------
    def is_alive(self) -> bool:
        """Check if the Neo4j connection is healthy.

        Returns:
            True if the driver can verify connectivity, False otherwise.
        """

        try:
            self.driver.verify_connectivity()
            return True
        except Exception:
            return False
