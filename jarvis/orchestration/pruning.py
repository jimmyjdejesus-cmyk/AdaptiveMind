"""Pruning manager with safety and reliability features.

Provides two-phase pruning (dry-run and commit), snapshot/rollback,
HITL prompts, and policy guardrails.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import json
import os
from typing import Any, Dict, List, Optional


@dataclass
class PruneRecord:
    """Audit record for prune/merge actions."""

    team: str
    actor: str
    reason: str
    timestamp: str


@dataclass
class PruningManager:
    """Manage safe, reversible team pruning operations."""

    state_store: Dict[str, Any]
    snapshots_dir: str = "snapshots"
    active_teams: List[str] = field(default_factory=list)
    lineage: List[PruneRecord] = field(default_factory=list)
    bq_approved: bool = False

    def __post_init__(self) -> None:
        os.makedirs(self.snapshots_dir, exist_ok=True)
        if not self.active_teams:
            self.active_teams = list(self.state_store.keys())

    # ----------------- Guardrails -----------------
    def _check_guardrails(self, team: str, context: Optional[Dict[str, Any]] = None) -> None:
        context = context or {}
        if team == "Security" and context.get("round") == "adversarial":
            raise ValueError("Cannot prune Security team during adversarial rounds.")
        if len(self.active_teams) <= 2 and not self.bq_approved:
            raise ValueError("At least two teams must remain active until BQ approval.")

    # ----------------- Two Phase Merge -----------------
    def dry_run(self, team: str, reason: str, actor: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Validate prune without changing state."""
        self._check_guardrails(team, context)
        return {
            "team": team,
            "reason": reason,
            "actor": actor,
            "snapshot_required": True,
        }

    def commit(self, team: str, reason: str, actor: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute prune after a successful dry run."""
        plan = self.dry_run(team, reason, actor, context)
        snapshot = self.snapshot_before_prune(team)
        state = self.state_store.pop(team, None)
        if team in self.active_teams:
            self.active_teams.remove(team)
        record = PruneRecord(team, actor, reason, datetime.utcnow().isoformat())
        self.lineage.append(record)
        return {"plan": plan, "snapshot": snapshot, "state": state}

    # ----------------- Snapshot / Rollback -----------------
    def _snapshot_path(self, team: str) -> str:
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return os.path.join(self.snapshots_dir, f"{team}_{ts}.json")

    def snapshot_before_prune(self, team: str) -> str:
        path = self._snapshot_path(team)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.state_store.get(team), fh)
        return path

    def rollback(self, snapshot_path: str, team: str) -> Dict[str, Any]:
        with open(snapshot_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self.state_store[team] = data
        if team not in self.active_teams:
            self.active_teams.append(team)
        return data

    # ----------------- HITL -----------------
    def generate_hitl_prompt(self, team: str, reason: str, score: Optional[float] = None, override_minutes: int = 10) -> str:
        detail = f"Prune Team {team}? Reason: {reason}"
        if score is not None:
            detail += f" ({score})"
        return f"{detail}. Override {override_minutes}m / Merge / Cancel"

    # ----------------- Lineage -----------------
    def audit_log(self) -> List[Dict[str, Any]]:
        return [record.__dict__ for record in self.lineage]
