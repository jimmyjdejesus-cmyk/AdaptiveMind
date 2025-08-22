import os
import sys

sys.path.append(os.getcwd())

from jarvis.ecosystem.meta_intelligence import ExecutiveAgent


def test_constitutional_critic_vetoes_blocked_plan():
    agent = ExecutiveAgent("exec_test")

    def fake_plan(goal: str):
        return ["DROP TABLE users"]

    agent.mission_planner.plan = fake_plan  # type: ignore
    result = agent.manage_directive("bad goal")
    assert result["success"] is False
    assert result["critique"]["veto"] is True
