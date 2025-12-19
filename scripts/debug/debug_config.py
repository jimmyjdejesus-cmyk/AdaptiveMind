#!/usr/bin/env python3.11
"""Debug script to check configuration loading."""

from adaptivemind_core.config import AppConfig, load_config


def debug_config():

    try:
        # Test direct config creation
        AppConfig()

        # Test load_config
        load_config()

        # Check environment variables

    except Exception:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_config()
