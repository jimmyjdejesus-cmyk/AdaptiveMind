#!/usr/bin/env python3
"""Fixed AdaptiveMind AI Server Startup Script with Correct Model Configuration."""

import os
import sys
from pathlib import Path

import uvicorn


def setup_environment():
    """Setup environment and check dependencies."""
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))

    return True

def load_fixed_config():
    """Load configuration with correct Ollama model."""
    try:
        from adaptivemind_core.config import (
            AppConfig,
            ContextPipelineConfig,
            MonitoringConfig,
            OllamaConfig,
            OpenRouterConfig,
            SecurityConfig,
            WindowsMLConfig,
        )

        config = AppConfig(
            ollama=OllamaConfig(
                host="http://127.0.0.1:11434",
                model="qwen3:0.6b",  # Use actual available model
                timeout=30.0,
                enable_ui=True
            ),
            openrouter=OpenRouterConfig(
                api_key="",
                model="openai/gpt-3.5-turbo",
                site_url="",
                app_name="AdaptiveMind Local"
            ),
            windowsml=WindowsMLConfig(enabled=False),
            security=SecurityConfig(api_keys=[]),
            context_pipeline=ContextPipelineConfig(
                enable_semantic_chunking=True,
                max_combined_context_tokens=8192
            ),
            monitoring=MonitoringConfig(
                enable_metrics_harvest=False
            ),
            allowed_personas=["generalist"],
            enable_research_features=False
        )
        return config

    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)

def start_fixed_server():
    """Start the fixed AdaptiveMind AI server."""
    setup_environment()
    config = load_fixed_config()

    try:
        from adaptivemind_core.server import build_app
        app = build_app(config)
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Start server
    port = int(os.getenv("ADAPTIVEMIND_PORT", "8000"))
    host = os.getenv("ADAPTIVEMIND_HOST", "127.0.0.1")


    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        pass
    except Exception:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_fixed_server()
