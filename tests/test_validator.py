#!/usr/bin/env python3.11
"""
Test the validator logic directly
"""

import sys
sys.path.insert(0, '')

from adaptivemind_core.config import AppConfig

def test_validator():
    print("🧪 Testing validator logic...")
    
    # Test empty list condition
    empty_list = []
    print(f"Empty list [] evaluates to: {bool(empty_list)}")
    print(f"Non-empty list ['test'] evaluates to: {bool(['test'])}")
    
    # Test AppConfig creation with default personas
    try:
        config = AppConfig()
        print(f"AppConfig created with personas: {list(config.personas.keys())}")
        print(f"AppConfig created with allowed_personas: {config.allowed_personas}")
    except Exception as e:
        print(f"AppConfig creation failed: {e}")

if __name__ == "__main__":
    test_validator()
