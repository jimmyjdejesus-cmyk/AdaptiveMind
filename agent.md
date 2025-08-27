# Development Log

- Created agent.md to log actions for repository updates.
- Documented Neo4j environment variables in config/default.yaml and deployment guide.
- Added input validation in Neo4jGraph and HierarchicalHypergraph to prevent injection attacks.
- Added unit tests for Neo4j credential loading and query sanitization.
- Implemented and passed unit tests (`pytest`).

- Added detailed docstrings to Neo4jGraph helpers and Hypergraph.update_node for maintainability.
- Expanded docstrings for Hypergraph query and mutation helpers.
- Added integration test skeleton for Neo4j that runs when a database is available.
- Surfaced Neo4j credential fields in the desktop app settings and documented secret-manager usage.
