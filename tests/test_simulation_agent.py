import asyncio
from pathlib import Path
import os
import sys

import pytest

sys.path.append(os.getcwd())

from jarvis.agents import SimulationAgent
from benchmarks import BenchmarkScenario


@pytest.mark.asyncio
async def test_run_plan_returns_forecast_and_logs(tmp_path):
    async def scenario(ctx):
        await asyncio.sleep(0)
        return "hello world"

    agent = SimulationAgent(repo_root=Path.cwd())
    plan = [["status"]]
    scenarios = [BenchmarkScenario(name="demo", fn=scenario)]

    result = await agent.run_plan(plan, scenarios)

    assert any("git status" in log for log in result.logs)
    assert "demo" in result.forecast
    assert result.forecast["demo"].token_count == 2
