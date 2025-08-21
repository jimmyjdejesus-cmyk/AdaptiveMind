"""Core Jarvis package used in tests.

The original project exposes a large surface area with optional imports and
runtime configuration.  For the purposes of the unit tests in this kata we keep
the package lightweight and only expose minimal metadata.  Individual modules
can still be imported directly, e.g. ``jarvis.ecosystem.meta_intelligence``.
"""

__all__ = ["__version__"]

__version__ = "4.0.0"

