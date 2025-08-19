"""
Core configuration settings for Jarvis AI V2
"""

# Default configuration
DEFAULT_CONFIG = {
    "enabled": True,
    "backend_url": "http://localhost:8001",
    "langgraph_checkpoint_path": "./checkpoints/jarvis_agent.db",
    "max_iterations": 15,
    "expert_model": "llama3.2",
    "use_langchain_tools": True,
    "fallback_to_v1": True,
    "workflow_visualization": True,
    "langgraphui_enabled": False
}

# Model configuration
MODELS = {
    "default": "llama3.2",
    "fallback": "gpt-4o",
    "specialist": "llama3.2-70b"
}

# Tool configuration
TOOLS_ENABLED = [
    "search",
    "code_analysis", 
    "web_browse",
    "file_management",
    "calculator"
]
