"""WhiteGate edge-case tests for MultiTeamOrchestrator."""

from typing import Any, Dict

import pytest
from jarvis.critics import CriticVerdict
from jarvis.orchestration.graph import MultiTeamOrchestrator


class DummyAgent:
    def __init__(self, team: str, result: Any):
        self.team = team
        self.result = result
        self.called = False

    def log(self, message: str, data: Dict[str, Any] | None = None):
        """No-op log method used by tests."""

    def run(self, objective: str, context: Dict[str, Any]):
        """Record invocation and return preset result."""
        self.called = True
        return self.result


class DummyOrchestrator:
    def __init__(self, teams):
        self.teams = teams
        self.team_status = {
            name: "running"
            for name in ["Red", "Blue", "Yellow", "Green", "White", "Black"]
        }

    def log(self, message: str, data: Dict[str, Any] | None = None):
        """No-op orchestrator log."""

    def broadcast(self, message: str, data: Dict[str, Any] | None = None):
        """No-op broadcast used by tests."""


@pytest.fixture
def orchestrator_builder():
    """Build a MultiTeamOrchestrator with configurable critic outputs."""

    def _build(red_output: Any, blue_output: Any):
        red_agent = DummyAgent("Red", red_output)
        blue_agent = DummyAgent("Blue", blue_output)
        yellow_agent = DummyAgent("Yellow", {})
        green_agent = DummyAgent("Green", {})
        black_agent = DummyAgent("Black", {})
        white_agent = DummyAgent("White", {})
        orch = DummyOrchestrator(
            {
                "adversary_pair": (red_agent, blue_agent),
                "competitive_pair": (yellow_agent, green_agent),
                "security_quality": white_agent,
                "innovators_disruptors": black_agent,
            }
        )
        return MultiTeamOrchestrator(orch), black_agent, white_agent

    return _build


def test_white_gate_blocks_downstream_when_rejected(orchestrator_builder):
    """Red critic rejection blocks innovators from executing."""
    red_verdict = CriticVerdict(approved=False, fixes=[], risk=0.2, notes="")
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    orchestrator, black_agent, _white_agent = orchestrator_builder(
        red_verdict, blue_verdict
    )
    orchestrator.run("test objective")
    assert not black_agent.called


def test_white_gate_allows_downstream_when_approved(orchestrator_builder):
    """Approval from both critics allows innovators to execute."""
    red_verdict = CriticVerdict(approved=True, fixes=[], risk=0.0, notes="")
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    orchestrator, black_agent, _white_agent = orchestrator_builder(
        red_verdict, blue_verdict
    )
    orchestrator.run("test objective")
    assert black_agent.called


def test_white_gate_accepts_dict_outputs(orchestrator_builder):
    """Critic verdicts provided as dicts are converted appropriately."""
    red_dict = {"approved": True, "risk": 0.0, "notes": ""}
    blue_dict = {"approved": True, "risk": 0.1, "notes": ""}
    orchestrator, black_agent, _white_agent = orchestrator_builder(
        red_dict, blue_dict
    )
    result = orchestrator.run("objective")
    assert black_agent.called
    assert result["halt"] is False


def test_white_gate_handles_unexpected_output_type(orchestrator_builder):
    """Non-dict/non-verdict outputs cause rejection and halt."""
    red_output = "unexpected"
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    orchestrator, black_agent, _white_agent = orchestrator_builder(
        red_output, blue_verdict
    )
    result = orchestrator.run("objective")
    assert not black_agent.called
    assert result["halt"] is True


def test_white_gate_calls_security_quality_always(orchestrator_builder):
    """Security-quality agent should run regardless of approval status."""
    red_verdict = CriticVerdict(approved=False, fixes=[], risk=0.2, notes="")
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    orchestrator, _black_agent, white_agent = orchestrator_builder(
        red_verdict, blue_verdict
    )
    orchestrator.run("objective")
    assert white_agent.called


def test_white_gate_defaults_missing_fields(orchestrator_builder):
    """Missing fields default to rejection without crashing."""
    red_dict = {}
    blue_dict = {"risk": 0.0}
    orchestrator, black_agent, _white_agent = orchestrator_builder(
        red_dict, blue_dict
    )
    result = orchestrator.run("objective")
    assert not black_agent.called
    assert result["halt"] is True


def test_white_gate_handles_malformed_verdict(orchestrator_builder):
    """Invalid field types result in rejection and safe defaults."""
    red_dict = {"approved": True, "risk": "high"}
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    orchestrator, black_agent, _white_agent = orchestrator_builder(
        red_dict, blue_verdict
    )
    result = orchestrator.run("objective")
    assert not black_agent.called
    assert result["halt"] is True
    assert result["critics"]["white_gate"]["risk"] == 1.0
