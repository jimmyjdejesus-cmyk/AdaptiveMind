# AdaptiveMind Framework
# Copyright (c) 2025 Jimmy De Jesus
# Licensed under CC-BY 4.0
#
# AdaptiveMind - Intelligent AI Routing & Context Engine
# More info: https://github.com/[username]/adaptivemind
# License: https://creativecommons.org/licenses/by/4.0/




# Copyright (c) 2025 Jimmy De Jesus (Bravetto)

# Licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0).
# See https://creativecommons.org/licenses/by/4.0/ for license terms.

"""Compatibility shim for legacy Jarvis_Local imports.

This module maintains backward compatibility by re-exporting the AdaptiveMind_Local package.
Code importing `Jarvis_Local` will receive a deprecation warning and should migrate to
`apps.AdaptiveMind_Local`.
"""
from __future__ import annotations

import importlib
import warnings
from types import ModuleType

warnings.warn(
    "The `Jarvis_Local` import path is deprecated. "
    "Please use `apps.AdaptiveMind_Local` instead. "
    "This compatibility shim will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2
)

_mod = importlib.import_module("apps.AdaptiveMind_Local")

# Re-export attributes from the real module so `import Jarvis_Local` behaves like before
for _name, _val in vars(_mod).items():
    if _name.startswith("__"):
        continue
    globals()[_name] = _val

# Make this module a package proxy for pkgutil-style imports
__path__ = getattr(_mod, "__path__", [])
__all__ = getattr(_mod, "__all__", [])
