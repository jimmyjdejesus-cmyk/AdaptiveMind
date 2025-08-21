"""
Jarvis AI - A privacy-first, modular AI assistant.
"""
from __future__ import annotations
import logging

# Version and author information
__version__ = "5.0.0" # Updated version to reflect major refactor
__author__ = "Jimmy De Jesus"

# Default configuration flags
DEFAULT_MCP_ENABLED = True
DEFAULT_MULTI_AGENT_ENABLED = True
DEFAULT_WORKFLOWS_ENABLED = True

# --- Other Components ---
try:
    from .agents.coding_agent import CodingAgent
except ImportError:
    CodingAgent = None

try:
    from .database.db_manager import DatabaseManager, get_database_manager
except ImportError:
    DatabaseManager = None
    get_database_manager = None

try:
    from .auth.security_manager import SecurityManager, get_security_manager
except ImportError:
    SecurityManager = None
    get_security_manager = None

try:
    from .workflows import WorkflowEngine, WorkflowTemplates
except ImportError:
    WorkflowEngine = None
    WorkflowTemplates = None


# --- Main Agent Factory ---

def get_jarvis_agent(
    enable_mcp: bool | None = None,
    enable_multi_agent: bool | None = None,
    enable_workflows: bool | None = None,
):
    """
    Get a Jarvis agent with configurable capabilities.

    This factory function is the primary entry point for creating a Jarvis agent.

    Args:
        enable_mcp: Explicitly enable or disable MCP.
        enable_multi_agent: Explicitly enable or disable multi-agent features.
        enable_workflows: Explicitly enable or disable workflow features.

    Returns:
        An instance of the unified Jarvis agent.

    Raises:
        ImportError: If the unified JarvisAgent is not available.
    """
    from .core.agent import JarvisAgent

    if not JarvisAgent:
        raise ImportError("The unified JarvisAgent is not available. Please check your installation.")

    # Set configuration based on defaults or explicit parameters
    config = {
        "enable_mcp": enable_mcp if enable_mcp is not None else DEFAULT_MCP_ENABLED,
        "enable_multi_agent": enable_multi_agent if enable_multi_agent is not None else DEFAULT_MULTI_AGENT_ENABLED,
        "enable_workflows": enable_workflows if enable_workflows is not None else DEFAULT_WORKFLOWS_ENABLED,
    }

    return JarvisAgent(**config)


# --- Convenience Functions ---

def get_simple_jarvis():
    """Get a basic Jarvis agent with only simple chat capabilities."""
    return get_jarvis_agent(enable_mcp=False, enable_multi_agent=False, enable_workflows=False)

def get_smart_jarvis():
    """Get a Jarvis agent with multi-model (MCP) routing."""
    return get_jarvis_agent(enable_mcp=True, enable_multi_agent=False, enable_workflows=False)

def get_super_jarvis():
    """Get a Jarvis agent with multi-agent orchestration."""
    return get_jarvis_agent(enable_mcp=True, enable_multi_agent=True, enable_workflows=False)

def get_ultimate_jarvis():
    """Get the most capable Jarvis agent with all features enabled."""
    return get_jarvis_agent(enable_mcp=True, enable_multi_agent=True, enable_workflows=True)


def get_coding_agent(base_agent=None, workspace_path: str | None = None):
    """
    Get an enhanced coding agent.
    """
    if not CodingAgent:
        logging.warning("CodingAgent is not available. Returning the base agent.")
        return base_agent or get_jarvis_agent()

    base_agent = base_agent or get_ultimate_jarvis()
    return CodingAgent(base_agent, workspace_path)


# --- Public API ---

__all__ = [
    # Main Factory and Unified Agent
    "get_jarvis_agent",
    # Convenience Wrappers
    "get_simple_jarvis",
    "get_smart_jarvis",
    "get_super_jarvis",
    "get_ultimate_jarvis",
    # Specialist Agents
    "get_coding_agent",
    "CodingAgent",
    # Supporting Systems
    "DatabaseManager",
    "get_database_manager",
    "SecurityManager",
    "get_security_manager",
    # Workflow Components
    "WorkflowEngine",
    "WorkflowTemplates",
]
