from typing import Any, Dict

from jarvis.critics import CriticVerdict
import pytest
from tests.test_black_team_context_isolation import _import_graph_module
from jarvis.critics import CriticVerdict as RealCriticVerdict


@pytest.fixture
def graph_module():
    with _import_graph_module() as module:
        module.CriticVerdict = RealCriticVerdict

        class StubWhiteGate:  # pragma: no cover - stub
            def merge(self, red, blue):
                return red if not red.approved else blue

        module.WhiteGate = StubWhiteGate

        class DummyGraph:  # pragma: no cover - stub
            def stream(self, *_args, **_kwargs):
                return []

        module.MultiTeamOrchestrator._build_graph = (
            lambda self: DummyGraph()
        )
        yield module


class DummyAgent:
    def __init__(self, team: str, result: Any):
        self.team = team
        self.result = result
        self.called = False

    def log(self, message: str, data: Dict[str, Any] | None = None):
        pass

    def run(self, objective: str, context: Dict[str, Any]):
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
        pass

    def broadcast(self, message: str, data: Dict[str, Any] | None = None):
        pass


def build_orchestrator(
    red_verdict: CriticVerdict,
    blue_verdict: CriticVerdict,
    graph_module,
):
    red_agent = DummyAgent("Red", red_verdict)
    blue_agent = DummyAgent("Blue", blue_verdict)
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
    return graph_module.MultiTeamOrchestrator(orch), black_agent


def test_white_gate_blocks_downstream_when_rejected(graph_module):
    red_verdict = CriticVerdict(approved=False, fixes=[], risk=0.2, notes="")
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    orchestrator, black_agent = build_orchestrator(
        red_verdict, blue_verdict, graph_module
    )
    state = {
        "objective": "test",
        "context": {},
        "team_outputs": {},
        "critics": {},
    }
    state = orchestrator._run_adversary_pair(state)
    assert state["halt"]
    assert not black_agent.called


def test_white_gate_allows_downstream_when_approved(graph_module):
    red_verdict = CriticVerdict(approved=True, fixes=[], risk=0.0, notes="")
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    orchestrator, black_agent = build_orchestrator(
        red_verdict, blue_verdict, graph_module
    )
    state = {
        "objective": "test",
        "context": {},
        "team_outputs": {},
        "critics": {},
    }
    state = orchestrator._run_adversary_pair(state)
    assert not state["halt"]
    orchestrator._run_innovators_disruptors(state)
    assert black_agent.called
