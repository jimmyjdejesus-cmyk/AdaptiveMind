from __future__ import annotations

"""Simulation agent to evaluate plans in a sandbox and forecast results."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

from jarvis.tools.git_sandbox import run_git_command
from benchmarks import BenchmarkRunner, BenchmarkScenario, Metric


@dataclass
class SimulationResult:
    """Outcome returned by :class:`SimulationAgent`."""

    forecast: Dict[str, Metric]
    logs: List[str]


class SimulationAgent:
    """Execute mission plans in a sandbox and provide performance forecasts."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)

    async def run_plan(
        self, plan: Iterable[Iterable[str]], scenarios: List[BenchmarkScenario]
    ) -> SimulationResult:
        """Simulate a plan and benchmark its impact.

        Parameters
        ----------
        plan:
            Iterable of git argument sequences. Each sequence is passed to
            :func:`run_git_command` with ``dry_run`` enabled to ensure no
            repository modifications occur.
        scenarios:
            Benchmark scenarios used to measure the forecasted performance.
        """

        logs: List[str] = []
        for args in plan:
            cmd = run_git_command(args, repo_root=self.repo_root, dry_run=True)
            logs.append(cmd)

        runner = BenchmarkRunner(scenarios)
        metrics = await runner.run(policy="balanced")
        return SimulationResult(forecast=metrics, logs=logs)


__all__ = ["SimulationAgent", "SimulationResult"]
