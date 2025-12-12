from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
import uuid


@dataclass
class DAGPlaceholder:
    mission_id: str
    steps: list


class MissionPlanner:
    def __init__(self, missions_dir: str | None = None) -> None:
        self.missions_dir = missions_dir

    def plan(self, goal: str, context: Dict[str, Any]) -> DAGPlaceholder:
        # Create a trivial DAG object with a deterministic mission ID
        mission_id = str(uuid.uuid4())
        return DAGPlaceholder(mission_id=mission_id, steps=[{"goal": goal}])
