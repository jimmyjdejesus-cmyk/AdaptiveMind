"""Compatibility shim for legacy `audit` package name.

This re-exports the audit subpackage provided under `adaptivemind_core.audit` so
that tests and external code importing `audit.*` continue to work during the
rebranding transition.
"""
from __future__ import annotations

from adaptivemind_core.audit import *  # noqa: F401,F403

__all__ = [name for name in globals().keys() if not name.startswith("_")]
