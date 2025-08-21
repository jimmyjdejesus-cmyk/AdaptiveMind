"""
Jarvis AI Agents - Specialized AI assistants and expert agents
"""

# Legacy coding agent
try:
    from .coding_agent import CodingAgent, get_coding_agent
except Exception:  # pragma: no cover
    CodingAgent = None

    def get_coding_agent(*args, **kwargs):  # type: ignore
        raise ImportError("CodingAgent not available")

# New specialist agents
try:
    from .specialist import SpecialistAgent
    from .specialists import (
        CodeReviewAgent,
        SecurityAgent, 
        ArchitectureAgent,
        TestingAgent,
        DevOpsAgent
    )
    
    # Add specialist agents to exports
    __all__ = [
        'CodingAgent', 
        'get_coding_agent',
        'SpecialistAgent',
        'CodeReviewAgent',
        'SecurityAgent',
        'ArchitectureAgent', 
        'TestingAgent',
        'DevOpsAgent'
    ]
    
except Exception:  # pragma: no cover
    # Fallback if specialist agents not available
    __all__ = ['CodingAgent', 'get_coding_agent']

# Version info
__version__ = "2.0.0"
__author__ = "Jarvis AI Team"

