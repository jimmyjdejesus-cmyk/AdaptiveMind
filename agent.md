# Agent Log

- Created agent.md to document changes and actions.
- Added `get_mission_history` method to `jarvis/world_model/neo4j_graph.py` with sanitization.
- Created FastAPI endpoint `/missions/{mission_id}/history` in `app/main.py`.
- Implemented frontend `MissionHistoryView` and integrated into `App.jsx`.
- Added unit tests for mission history retrieval.
- Added configurable backend URL with status indicators in MissionHistoryView.
- Extended /health endpoint to report Neo4j connectivity.
- Added Neo4jGraph.is_alive method and accompanying tests.
- Introduced lightweight FastAPI test harness (`app/test_harness.py`) to avoid heavy imports in endpoint tests.
- Added `tests/test_api.py` using the harness to verify mission history and health endpoints without side effects.
