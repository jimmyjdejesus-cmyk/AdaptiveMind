"""Lightweight agents package used in tests.

Only a small subset of the full project agents are exposed here with guarded
imports to avoid heavy optional dependencies during testing.
"""

from __future__ import annotations

# Core planning and curiosity utilities
try:  # pragma: no cover - optional dependencies
    from .mission_planner import MissionPlanner
except Exception:  # pragma: no cover
    MissionPlanner = None  # type: ignore

try:  # pragma: no cover - optional dependencies
    from .curiosity_agent import CuriosityAgent
except Exception:  # pragma: no cover
    CuriosityAgent = None  # type: ignore

# Optional specialist agents – failure to import simply leaves them as ``None``
try:  # pragma: no cover
    from .coding_agent import CodingAgent, get_coding_agent
except Exception:  # pragma: no cover
    CodingAgent = None  # type: ignore

    def get_coding_agent(*_args, **_kwargs):  # type: ignore
        raise ImportError("CodingAgent not available")

from .base_specialist import BaseSpecialist  # noqa: F401

try:  # pragma: no cover - optional dependencies
    from .simulation_agent import SimulationAgent  # noqa: F401
except Exception:  # pragma: no cover
    SimulationAgent = None  # type: ignore

try:  # pragma: no cover - optional dependencies
    from .monte_carlo_explorer import MonteCarloExplorer  # noqa: F401
except Exception:  # pragma: no cover
    MonteCarloExplorer = None  # type: ignore

try:  # pragma: no cover - optional dependencies
    from .benchmark_agent import BenchmarkRewardAgent  # noqa: F401
except Exception:  # pragma: no cover
    BenchmarkRewardAgent = None  # type: ignore

try:  # pragma: no cover - optional dependencies
    from .decentralized_actor import DecentralizedActor  # noqa: F401
except Exception:  # pragma: no cover
    DecentralizedActor = None  # type: ignore

try:
    from .live_test_agent import LiveTestAgent  # noqa: F401
except Exception:  # pragma: no cover
    LiveTestAgent = None

# New specialist agents
try:
    from .specialist import SpecialistAgent  # noqa: F401
    from .specialists import (  # noqa: F401
        CodeReviewAgent,
        ArchitectureAgent,
        TestingAgent,
        DevOpsAgent,
        CloudCostOptimizerAgent,
        UserFeedbackAgent,
    )
    from .critics import RedTeamCritic  # noqa: F401

    # Add specialist agents to exports
    __all__ = [
        'CodingAgent',
        'get_coding_agent',
        'MissionPlanner',
        'BaseSpecialist',
        'SimulationAgent',
        'MonteCarloExplorer',
        'CuriosityAgent',
        'BenchmarkRewardAgent',
        'LiveTestAgent',
        'SpecialistAgent',
        'CodeReviewAgent',
        'ArchitectureAgent',
        'TestingAgent',
        'DevOpsAgent',
        'CloudCostOptimizerAgent',
        'UserFeedbackAgent',
        'RedTeamCritic',
        'DecentralizedActor'
    ]

except Exception:  # pragma: no cover
    # Fallback if specialist agents not available
    __all__ = [
        'CodingAgent',
        'get_coding_agent',
        'MissionPlanner',
        'SimulationAgent',
        'MonteCarloExplorer',
        'CuriosityAgent',
        'BenchmarkRewardAgent',
        'LiveTestAgent',
        'DecentralizedActor',
    ]
