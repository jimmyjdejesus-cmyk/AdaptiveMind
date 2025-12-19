#!/usr/bin/env python3

# AdaptiveMind Framework
# Copyright (c) 2025 Jimmy De Jesus
# Licensed under CC-BY 4.0
#
# AdaptiveMind - Intelligent AI Routing & Context Engine
# More info: https://github.com/[username]/adaptivemind
# License: https://creativecommons.org/licenses/by/4.0/



"""
Test script for OpenRouter integration
Run this to verify your OpenRouter setup works correctly
"""

import os
import sys

# Add the legacy path to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'legacy'))

def test_openrouter_connection():
    """Test basic OpenRouter connection"""

    # Check if API key is set
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return False

    if not api_key.startswith("sk-or-v1"):
        return False

    try:
        from adaptivemind.mcp.providers.openrouter import OpenRouterClient


        client = OpenRouterClient(api_key=api_key)

        # Test a simple request
        client.generate("Say 'Hello from OpenRouter!' in exactly 5 words.")


        # Check cost status
        client.get_cost_status()

        return True

    except ImportError:
        return False

    except Exception:
        return False

def test_model_router():
    """Test the model router integration"""

    try:
        from adaptivemind.mcp.model_router import ModelRouter


        # Create mock MCP client (we'll only test OpenRouter part)
        mcp_client = None  # We'll modify router to work without full MCP

        # For now, just test the complexity classification
        router = ModelRouter(mcp_client)

        test_prompts = [
            "Hello world",  # Should be low
            "Write a Python function to calculate fibonacci numbers",  # Should be medium
            "Design a secure authentication system for a web application",  # Should be high
        ]

        for prompt in test_prompts:
            router._classify_complexity(prompt, "general")

        return True

    except Exception:
        return False

def main():
    """Run all tests"""

    # Test 1: OpenRouter Connection
    openrouter_ok = test_openrouter_connection()

    # Test 2: Model Router (basic functionality)
    router_ok = test_model_router()


    if openrouter_ok and router_ok:
        pass
    else:
        pass

if __name__ == "__main__":
    main()
