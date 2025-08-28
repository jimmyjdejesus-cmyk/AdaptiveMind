import importlib.util
import pathlib
import sys
import time
import types
import contextlib

import asyncio
import pytest


@contextlib.contextmanager
def _import_graph_module():
    root = pathlib.Path(__file__).resolve().parents[1] / "jarvis"

    jarvis_stub = types.ModuleType("jarvis")
    jarvis_stub.__path__ = [str(root)]
    orchestration_stub = types.ModuleType("jarvis.orchestration")
    orchestration_stub.__path__ = [str(root / "orchestration")]

    team_agents_stub = types.ModuleType("jarvis.orchestration.team_agents")

    class OrchestratorAgent:  # pragma: no cover - stub
        pass

    class TeamMemberAgent:  # pragma: no cover - stub
        pass

    team_agents_stub.OrchestratorAgent = OrchestratorAgent
    team_agents_stub.TeamMemberAgent = TeamMemberAgent

    pruning_stub = types.ModuleType("jarvis.orchestration.pruning")

    class PruningEvaluator:  # pragma: no cover - stub
        def should_prune(self, *args, **kwargs):
            return False

    pruning_stub.PruningEvaluator = PruningEvaluator

    critics_stub = types.ModuleType("jarvis.critics")

    class CriticVerdict:  # pragma: no cover - stub
        pass

    class WhiteGate:  # pragma: no cover - stub
        def merge(self, red, blue):
            return CriticVerdict()

    class RedTeamCritic:  # pragma: no cover - stub
        async def review(self, *args, **kwargs):
            return CriticVerdict()

    class BlueTeamCritic:  # pragma: no cover - stub
        async def review(self, *args, **kwargs):
            return CriticVerdict()

    critics_stub.CriticVerdict = CriticVerdict
    critics_stub.WhiteGate = WhiteGate
    critics_stub.RedTeamCritic = RedTeamCritic
    critics_stub.BlueTeamCritic = BlueTeamCritic

    langgraph_graph = types.ModuleType("langgraph.graph")

    class StateGraph:  # pragma: no cover - stub
        def __init__(self, *args, **kwargs):
            pass

        def add_node(self, *args, **kwargs):
            pass

        def set_entry_point(self, *args, **kwargs):
            pass

        def add_edge(self, *args, **kwargs):
            pass

        def compile(self):
            return self

        def stream(self, *_args, **_kwargs):
            return []

    langgraph_graph.StateGraph = StateGraph
    langgraph_graph.END = object()
    langgraph_pkg = types.ModuleType("langgraph")
    langgraph_pkg.graph = langgraph_graph

    stubs = {
        "jarvis": jarvis_stub,
        "jarvis.orchestration": orchestration_stub,
        "jarvis.orchestration.team_agents": team_agents_stub,
        "jarvis.orchestration.pruning": pruning_stub,
        "jarvis.critics": critics_stub,
        "langgraph.graph": langgraph_graph,
        "langgraph": langgraph_pkg,
    }

    saved = {}
    try:
        for name, module in stubs.items():
            saved[name] = sys.modules.get(name)
            sys.modules[name] = module
        spec = importlib.util.spec_from_file_location(
            "jarvis.orchestration.graph", root / "orchestration" / "graph.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        yield module
    finally:
        for name in stubs:
            if saved[name] is None:
                del sys.modules[name]
            else:
                sys.modules[name] = saved[name]


@pytest.fixture()
def graph_module():
    with _import_graph_module() as module:
        class DummyGraph:  # pragma: no cover - stub
            def stream(self, *_args, **_kwargs):
                return []

        module.MultiTeamOrchestrator._build_graph = (
            lambda self: DummyGraph()
        )
        yield module


class DummyBlackAgent:
    team = "Black"

    def __init__(self):
        self.received_context = None

    def run(self, objective, context):
        self.received_context = context
        return {"status": "ok"}

    def log(self, message, data=None):  # pragma: no cover - noop
        pass


class DummyOrchestrator:
    def __init__(self):
        self.teams = {"innovators_disruptors": DummyBlackAgent()}

    def log(self, *args, **kwargs):  # pragma: no cover - noop
        pass

    def broadcast(self, *args, **kwargs):  # pragma: no cover - noop
        pass


class DummyAgent:
    def __init__(self, team):
        self.team = team


class PairOrchestrator:
    def __init__(self):
        self.teams = {
            "competitive_pair": (
                DummyAgent("Yellow"),
                DummyAgent("Green"),
            )
        }

    def log(self, *args, **kwargs):  # pragma: no cover - noop
        pass

    def broadcast(self, *args, **kwargs):  # pragma: no cover - noop
        pass


def test_black_team_excludes_white_team_context(graph_module):
    orchestrator = DummyOrchestrator()
    mto = graph_module.MultiTeamOrchestrator(orchestrator)
    state = {
        "objective": "test",
        "context": {"foo": "bar", "leak": "secret"},
        "team_outputs": {"security_quality": {"leak": "classified"}},
    }

    mto._run_innovators_disruptors(state)

    received = orchestrator.teams["innovators_disruptors"].received_context
    assert "leak" not in received
    assert received["foo"] == "bar"


@pytest.mark.parametrize("white_output", [None, "ok", [1, 2], 42])
def test_black_team_handles_non_dict_white_output(graph_module, white_output):
    orchestrator = DummyOrchestrator()
    mto = graph_module.MultiTeamOrchestrator(orchestrator)
    state = {
        "objective": "test",
        "context": {"foo": "bar", "leak": "secret"},
        "team_outputs": {"security_quality": white_output},
    }

    mto._run_innovators_disruptors(state)

    received = orchestrator.teams["innovators_disruptors"].received_context
    assert received["leak"] == "secret"


def test_competitive_pair_runs_in_parallel(graph_module):
    orchestrator = PairOrchestrator()
    mto = graph_module.MultiTeamOrchestrator(orchestrator)

    async def fake_run(team, state):
        await asyncio.sleep(0.1)
        return {team.team: "ok"}

    mto._run_team_async = fake_run  # type: ignore
    state = {"objective": "test", "context": {}, "team_outputs": {}}
    start = time.perf_counter()
    mto._run_competitive_pair(state)
    elapsed = time.perf_counter() - start

    assert elapsed < 0.2
    assert len(state["team_outputs"]["competitive_pair"]) == 2
