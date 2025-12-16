"""Compatibility shim for `Jarvis_Local`.

This module exists temporarily to provide backwards compatibility for imports
that reference `Jarvis_Local`. Prefer importing `apps.Jarvis_Local` instead.
The shim emits a DeprecationWarning and re-exports the moved package.
"""
from __future__ import annotations
import warnings

warnings.warn(
    "`Jarvis_Local` moved to `apps.Jarvis_Local`. Import `apps.Jarvis_Local` instead. "
    "This shim will be removed in a future release.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export moved package for convenience; keep minimal to avoid heavy imports.
try:
    from apps import Jarvis_Local as _moved
    # Expose everything from the moved package
    import sys
    sys.modules["Jarvis_Local"] = _moved
except ImportError:
    pass
