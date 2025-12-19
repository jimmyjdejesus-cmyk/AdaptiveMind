#!/usr/bin/env python3
"""
Simple configuration validator test - bypassing server imports
"""

import sys

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

def _default_personas() -> dict[str, PersonaConfig]:
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
    personas: dict[str, PersonaConfig] = Field(default_factory=_default_personas)
    allowed_personas: list[str] = Field(default_factory=list)

    @field_validator("allowed_personas", mode="after")
    @classmethod
    def _default_allowed_personas(cls, value: list[str] | None, info: ValidationInfo) -> list[str]:
        """Set default allowed personas from configured personas if not explicitly set.

        This is the fixed validator - using 'is not None' instead of 'if value:'
        """
        if value is not None:
            return value
        personas = info.data.get("personas", {})
        if isinstance(personas, dict):
            persona_keys = list(personas.keys())
            return persona_keys
        return []

def test_config_with_empty_list():
    """Test configuration with empty allowed_personas list."""

    # Test case 1: Empty list should trigger default behavior
    config_data = {
        "personas": _default_personas(),
        "allowed_personas": []  # Empty list
    }

    try:
        config = AppConfig(**config_data)
        expected = ["generalist"]
        return config.allowed_personas == expected
    except Exception:
        return False

def test_config_with_none():
    """Test configuration with None allowed_personas."""

    # Test case 2: None should trigger default behavior
    config_data = {
        "personas": _default_personas(),
        "allowed_personas": None  # None value
    }

    try:
        config = AppConfig(**config_data)
        expected = ["generalist"]
        return config.allowed_personas == expected
    except Exception:
        return False

def test_config_with_explicit_values():
    """Test configuration with explicit allowed_personas."""

    # Test case 3: Explicit values should be preserved
    config_data = {
        "personas": _default_personas(),
        "allowed_personas": ["custom_persona"]  # Explicit values
    }

    try:
        config = AppConfig(**config_data)
        expected = ["custom_persona"]
        return config.allowed_personas == expected
    except Exception:
        return False

def test_config_default():
    """Test configuration with defaults (no allowed_personas specified)."""

    # Test case 4: Default behavior when not specified
    config_data = {
        "personas": _default_personas()
        # allowed_personas not specified at all
    }

    try:
        config = AppConfig(**config_data)
        expected = ["generalist"]
        return config.allowed_personas == expected
    except Exception:
        return False

def main():
    """Run all configuration tests."""

    tests = [
        test_config_with_empty_list,
        test_config_with_none,
        test_config_with_explicit_values,
        test_config_default
    ]

    results = []
    for test in tests:
        results.append(test())


    passed = sum(results)
    total = len(results)


    return passed == total

if __name__ == "__main__":
    main()
