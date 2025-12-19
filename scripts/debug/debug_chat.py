#!/usr/bin/env python3.11
"""Debug script to identify the exact error in chat functionality."""

from adaptivemind_core.app import AdaptiveMindApplication
from adaptivemind_core.config import load_config


def debug_chat():

    try:
        # Load configuration
        config = load_config()

        # Create application
        app = AdaptiveMindApplication(config=config)

        # Check personas
        app.personas()

        # Check routing config
        app.get_routing_config()

        # Check backends
        app.list_backends()

        # Test backend availability
        for backend in app.backends:
            backend.is_available()
            if hasattr(backend, 'get_available_models'):
                backend.get_available_models()

        # Try to test a simple chat
        try:
            app.chat(
                persona="generalist",
                messages=[{"role": "user", "content": "Hello, how are you?"}],
                temperature=0.7,
                max_tokens=100
            )

        except Exception:
            import traceback
            traceback.print_exc()

        # Cleanup
        app.shutdown()

    except Exception:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_chat()
