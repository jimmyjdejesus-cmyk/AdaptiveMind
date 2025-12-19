"""Minimal specialist registry shim.

This is a lightweight compatibility implementation intended for tests and
simple usage during the rebranding transition. The production registry
normally lives under the apps or is provided by test fixtures.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

_SPECIALIST_REGISTRY: dict[str, Callable[..., Any]] = {}


def get_specialist_registry() -> dict[str, Callable[..., Any]]:
    """Return a copy of the specialist registry."""
    return dict(_SPECIALIST_REGISTRY)


def create_specialist(name: str, factory: Callable[..., Any]) -> None:
    """Register a specialist factory under the given name."""
    _SPECIALIST_REGISTRY[name] = factory


def clear_registry() -> None:
    """Clear the registry (useful in tests)."""
    _SPECIALIST_REGISTRY.clear()
