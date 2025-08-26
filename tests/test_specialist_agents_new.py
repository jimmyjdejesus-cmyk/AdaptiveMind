import asyncio
import pathlib
import sys
import importlib.util
import types

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Minimal package setup to satisfy relative imports without heavy dependencies
jarvis_spec = importlib.util.spec_from_file_location("jarvis", ROOT / "jarvis" / "__init__.py")
jarvis_pkg = importlib.util.module_from_spec(jarvis_spec)
sys.modules["jarvis"] = jarvis_pkg
jarvis_spec.loader.exec_module(jarvis_pkg)

agents_pkg = types.ModuleType("jarvis.agents")
agents_pkg.__path__ = [str(ROOT / "jarvis" / "agents")]
sys.modules["jarvis.agents"] = agents_pkg

world_model_pkg = types.ModuleType("jarvis.world_model")
sys.modules["jarvis.world_model"] = world_model_pkg
kg_module = types.ModuleType("jarvis.world_model.knowledge_graph")
class _KG:  # minimal stub
    pass
kg_module.KnowledgeGraph = _KG
sys.modules["jarvis.world_model.knowledge_graph"] = kg_module

tools_pkg = types.ModuleType("jarvis.tools")
tools_pkg.__path__ = []
sys.modules["jarvis.tools"] = tools_pkg
sandbox_module = types.ModuleType("jarvis.tools.execution_sandbox")
class _ER:
    exit_code = 0
    stdout = ""
    stderr = ""
def _run_python_code(code: str):
    return _ER()
sandbox_module.run_python_code = _run_python_code
sandbox_module.ExecutionResult = _ER
sys.modules["jarvis.tools.execution_sandbox"] = sandbox_module

spec = importlib.util.spec_from_file_location(
    "jarvis.agents.specialists", ROOT / "jarvis" / "agents" / "specialists.py"
)
specialists = importlib.util.module_from_spec(spec)
sys.modules["jarvis.agents.specialists"] = specialists
spec.loader.exec_module(specialists)

DocumentationAgent = specialists.DocumentationAgent
DatabaseAgent = specialists.DatabaseAgent
LocalizationAgent = specialists.LocalizationAgent
EthicalHackerAgent = specialists.EthicalHackerAgent
CloudCostOptimizerAgent = specialists.CloudCostOptimizerAgent
UserFeedbackAgent = specialists.UserFeedbackAgent


@pytest.mark.parametrize(
    "agent_cls, method, args, header, specialization",
    [
        (DocumentationAgent, "generate_documentation", ("print('hi')", "Added feature"), "DOCUMENTATION REQUEST", "documentation"),
        (DatabaseAgent, "optimize_query", ("SELECT * FROM t", None), "QUERY OPTIMIZATION REQUEST", "database"),
        (LocalizationAgent, "translate_content", ("Hello", "es"), "LOCALIZATION REQUEST", "localization"),
        (EthicalHackerAgent, "penetration_test", ("test system",), "PENETRATION TEST REQUEST", "ethical_hacking"),
        (CloudCostOptimizerAgent, "analyze_usage", ("usage report",), "CLOUD COST ANALYSIS REQUEST", "cloud_cost"),
        (UserFeedbackAgent, "analyze_feedback", ("Great app but slow",), "USER FEEDBACK ANALYSIS REQUEST", "user_feedback"),
    ],
)
def test_specialist_agent_prompts(monkeypatch, agent_cls, method, args, header, specialization):
    """Ensure new specialist agents build proper prompts and call process_task."""
    captured = {}

    async def fake_process(self, task, *_, **__):
        captured["task"] = task
        return {"ok": True}

    monkeypatch.setattr(agent_cls, "process_task", fake_process)
    agent = agent_cls(mcp_client=None)

    assert agent.specialization == specialization

    result = asyncio.run(getattr(agent, method)(*args))
    assert result == {"ok": True}
    assert header in captured["task"]
