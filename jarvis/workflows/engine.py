from __future__ import annotations
from enum import Enum
from typing import Dict, Any


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


def evaluate_workflow(dag: Any) -> Dict[str, Any]:
    return {"status": WorkflowStatus.PENDING}
