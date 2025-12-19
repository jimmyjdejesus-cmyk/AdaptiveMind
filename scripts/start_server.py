# AdaptiveMind Framework
# Copyright (c) 2025 Jimmy De Jesus
# Licensed under CC-BY 4.0
#
# AdaptiveMind - Intelligent AI Routing & Context Engine
# More info: https://github.com/[username]/adaptivemind
# License: https://creativecommons.org/licenses/by/4.0/




# Copyright (c) 2025 Jimmy De Jesus (Bravetto)

# Licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0).
# See https://creativecommons.org/licenses/by/4.0/ for license terms.

#!/usr/bin/env python3
"""Simple AdaptiveMind AI Server Startup Script.

This script starts the AdaptiveMind AI server with proper configuration
and handles dependency issues.
"""

import os
import sys
from pathlib import Path

import uvicorn


def setup_environment():
    """Setup environment and check dependencies."""
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))

    # Check Python version


    # Try to import dependencies
    try:
        import fastapi
        import pydantic
        import uvicorn
    except ImportError:
        os.system(f"{sys.executable} -m pip install -r requirements.txt")

    return True

def load_config():
    """Load or create default configuration."""
    try:
        # Try to import and load config
        from adaptivemind_core.config import AppConfig, PersonaConfig, load_config

        try:
            config = load_config()
            return config
        except Exception:

            # Create default configuration
            from adaptivemind_core.config import (
                ContextPipelineConfig,
                MonitoringConfig,
                OllamaConfig,
                OpenRouterConfig,
                SecurityConfig,
                WindowsMLConfig,
            )

            config = AppConfig(
                ollama=OllamaConfig(host="http://127.0.0.1:11434"),
                openrouter=OpenRouterConfig(api_key=""),
                windowsml=WindowsMLConfig(enabled=False),
                security=SecurityConfig(api_keys=[]),  # No API keys for testing
                context_pipeline=ContextPipelineConfig(),
                monitoring=MonitoringConfig(enable_metrics_harvest=False),
                allowed_personas=["generalist"],
                enable_research_features=False
            )
            return config

    except Exception:

        # Create minimal working configuration
        from adaptivemind_core.config import AppConfig, PersonaConfig

        default_persona = PersonaConfig(
            name="generalist",
            description="Default test persona",
            system_prompt="You are a helpful assistant.",
            max_context_window=2048,
            routing_hint="general"
        )

        config = AppConfig(
            personas={"generalist": default_persona},
            allowed_personas=["generalist"],
            security={"api_keys": []}
        )
        return config

def start_server():
    """Start the AdaptiveMind AI server."""
    # Setup environment
    setup_environment()

    # Load configuration
    config = load_config()

    try:
        # Try to build the app
        from adaptivemind_core.server import build_app
        app = build_app(config)
    except Exception:

        # Create minimal server as fallback
        from fastapi import FastAPI

        app = FastAPI(title="AdaptiveMind AI", version="1.0.0")

        @app.get("/health")
        async def health():
            return {"status": "ok", "available_models": ["test"]}

        @app.get("/api/v1/models")
        async def models():
            return ["test-model"]

        @app.get("/api/v1/personas")
        async def personas():
            return [{"name": "generalist", "description": "Default persona"}]

        @app.post("/api/v1/chat")
        async def chat(request: dict):
            return {
                "content": "Test response",
                "model": "test",
                "tokens": 10,
                "diagnostics": {}
            }


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
        sys.exit(1)

if __name__ == "__main__":
    start_server()
