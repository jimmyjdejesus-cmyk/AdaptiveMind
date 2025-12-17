"""Adaptivemind agents compatibility package.

Provides minimal shims for `adaptivemind.agents.*` to satisfy imports
and for tests that patch these modules dynamically.
"""
from __future__ import annotations

__all__ = ["critics", "specialist_registry"]
