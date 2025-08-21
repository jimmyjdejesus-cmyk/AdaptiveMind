# Orchestration Package
"""
Multi-agent orchestration system for coordinating specialist AI agents

This package provides:
- MultiAgentOrchestrator: Coordinates multiple specialists for complex tasks
- SubOrchestrator: Scoped orchestrator used for nested missions
- Workflow management and task delegation
- Result synthesis and conflict resolution
"""

from .orchestrator import MultiAgentOrchestrator
from .sub_orchestrator import SubOrchestrator

__all__ = ['MultiAgentOrchestrator', 'SubOrchestrator']

# Version info
__version__ = "1.0.0"
__author__ = "Jarvis AI Team"
