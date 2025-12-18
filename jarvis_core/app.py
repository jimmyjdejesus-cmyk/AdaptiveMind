"""Compatibility shim for jarvis_core.app pointing to adaptivemind_core.app."""
from __future__ import annotations

from adaptivemind_core.app import *  # noqa: F401,F403

__all__ = [name for name in globals().keys() if not name.startswith("_")]
