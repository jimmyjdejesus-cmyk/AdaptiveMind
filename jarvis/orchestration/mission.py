from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Mission:
    id: str
    title: str
    goal: str
    inputs: Dict[str, Any]
    risk_level: str
    dag: Any


def save_mission(mission: Mission) -> None:
    """Persist mission metadata. For tests we perform a no-op persistence.
    This implementation exists to avoid import-time errors during tests.
    """
    # In a full runtime this would write to disk or a DB. For tests, no-op.
    return None
