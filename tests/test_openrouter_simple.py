#!/usr/bin/env python3

# AdaptiveMind Framework
# Copyright (c) 2025 Jimmy De Jesus
# Licensed under CC-BY 4.0
#
# AdaptiveMind - Intelligent AI Routing & Context Engine
# More info: https://github.com/[username]/adaptivemind
# License: https://creativecommons.org/licenses/by/4.0/



"""
Simple test for OpenRouter client without MCP dependencies
"""

import os
import sys


def test_openrouter_client():
    """Test OpenRouter client directly"""

    # Set a dummy API key for testing (will fail but test structure)
    test_key = os.getenv("OPENROUTER_API_KEY", "sk-or-v1-test-key")

    try:
        # Import just the OpenRouter client
        sys.path.append(os.path.join(os.path.dirname(__file__), 'legacy'))
        # Direct import to avoid MCP dependencies
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "openrouter",
            os.path.join(os.path.dirname(__file__), 'legacy', 'jarvis', 'mcp', 'providers', 'openrouter.py')
        )
        openrouter_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(openrouter_module)
        OpenRouterClient = openrouter_module.OpenRouterClient


        # Test client initialization
        client = OpenRouterClient(api_key=test_key)

        # Test model selection
        client.get_model_for_complexity("low")
        client.get_model_for_complexity("medium")
        client.get_model_for_complexity("high")


        # Test cost status
        client.get_cost_status()

        # Test complexity classification (mock router)
        class MockRouter:
            def _classify_complexity(self, prompt, task_type):
                # Simple mock implementation
                prompt_len = len(prompt)
                if prompt_len > 100:
                    return "high" if "architecture" in prompt.lower() else "medium"
                return "low"

        router = MockRouter()
        test_prompts = [
            "Hello",
            "Write a function",
            "Design a system architecture"
        ]

        for prompt in test_prompts:
            router._classify_complexity(prompt, "general")

        return True

    except ImportError:
        return False

    except Exception:
        return False

def main():
    """Run the simple test"""

    success = test_openrouter_client()

    if success:
        pass
    else:
        pass

if __name__ == "__main__":
    main()
