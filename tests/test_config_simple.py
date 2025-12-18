#!/usr/bin/env python3
"""
Simple configuration validator test - bypassing server imports
"""

import sys
import os
from typing import Dict, List
from pydantic import BaseModel, Field, ValidationInfo, field_validator

# Add the current directory to Python path
sys.path.insert(0, '')

class PersonaConfig(BaseModel):
    """Minimal persona config for testing."""
    name: str
    description: str
    system_prompt: str
    max_context_window: int = Field(4096, ge=512)
    routing_hint: str = Field("general", description="Hint used by the routing pipeline")

def _default_personas() -> Dict[str, PersonaConfig]:
    """Create default persona configurations."""
    default_persona = PersonaConfig(
        name="generalist",
        description="Balanced assistant persona",
        system_prompt=(
            "You are AdaptiveMind, a local-first research assistant. Provide concise, factual answers and highlight sources."
        ),
        max_context_window=4096,
    )
    return {default_persona.name: default_persona}

class AppConfig(BaseModel):
    """Minimal app config for testing the validator."""
    personas: Dict[str, PersonaConfig] = Field(default_factory=_default_personas)
    allowed_personas: List[str] = Field(default_factory=list)

    @field_validator("allowed_personas", mode="after")
    @classmethod
    def _default_allowed_personas(cls, value: List[str] | None, info: ValidationInfo) -> List[str]:
        """Set default allowed personas from configured personas if not explicitly set.
        
        This is the fixed validator - using 'is not None' instead of 'if value:'
        """
        if value is not None:
            print(f"DEBUG: value is not None: {value}")
            return value
        personas = info.data.get("personas", {})
        print(f"DEBUG: personas from info.data: {personas}")
        if isinstance(personas, dict):
            persona_keys = list(personas.keys())
            print(f"DEBUG: returning persona keys: {persona_keys}")
            return persona_keys
        print("DEBUG: returning empty list")
        return []

def test_config_with_empty_list():
    """Test configuration with empty allowed_personas list."""
    print("=== Testing Config with Empty List ===")
    
    # Test case 1: Empty list should trigger default behavior
    config_data = {
        "personas": _default_personas(),
        "allowed_personas": []  # Empty list
    }
    
    try:
        config = AppConfig(**config_data)
        print(f"SUCCESS: allowed_personas = {config.allowed_personas}")
        expected = ["generalist"]
        if config.allowed_personas == expected:
            print("✅ PASS: Empty list correctly populated with persona names")
            return True
        else:
            print(f"❌ FAIL: Expected {expected}, got {config.allowed_personas}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_config_with_none():
    """Test configuration with None allowed_personas."""
    print("\n=== Testing Config with None ===")
    
    # Test case 2: None should trigger default behavior
    config_data = {
        "personas": _default_personas(),
        "allowed_personas": None  # None value
    }
    
    try:
        config = AppConfig(**config_data)
        print(f"SUCCESS: allowed_personas = {config.allowed_personas}")
        expected = ["generalist"]
        if config.allowed_personas == expected:
            print("✅ PASS: None correctly populated with persona names")
            return True
        else:
            print(f"❌ FAIL: Expected {expected}, got {config.allowed_personas}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_config_with_explicit_values():
    """Test configuration with explicit allowed_personas."""
    print("\n=== Testing Config with Explicit Values ===")
    
    # Test case 3: Explicit values should be preserved
    config_data = {
        "personas": _default_personas(),
        "allowed_personas": ["custom_persona"]  # Explicit values
    }
    
    try:
        config = AppConfig(**config_data)
        print(f"SUCCESS: allowed_personas = {config.allowed_personas}")
        expected = ["custom_persona"]
        if config.allowed_personas == expected:
            print("✅ PASS: Explicit values correctly preserved")
            return True
        else:
            print(f"❌ FAIL: Expected {expected}, got {config.allowed_personas}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_config_default():
    """Test configuration with defaults (no allowed_personas specified)."""
    print("\n=== Testing Config with Defaults ===")
    
    # Test case 4: Default behavior when not specified
    config_data = {
        "personas": _default_personas()
        # allowed_personas not specified at all
    }
    
    try:
        config = AppConfig(**config_data)
        print(f"SUCCESS: allowed_personas = {config.allowed_personas}")
        expected = ["generalist"]
        if config.allowed_personas == expected:
            print("✅ PASS: Default behavior correctly populates persona names")
            return True
        else:
            print(f"❌ FAIL: Expected {expected}, got {config.allowed_personas}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all configuration tests."""
    print("Testing Configuration Validator Fix")
    print("=" * 50)
    
    tests = [
        test_config_with_empty_list,
        test_config_with_none, 
        test_config_with_explicit_values,
        test_config_default
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Configuration validator is working correctly.")
        return True
    else:
        print("❌ SOME TESTS FAILED! Configuration validator needs more work.")
        return False

if __name__ == "__main__":
    main()
