"""Utility and web tools for Jarvis AI.

This package exposes common tooling used across the Jarvis ecosystem,
including web research capabilities.
"""

from .repository_indexer import RepositoryIndexer
from .environment_tools import read_file, write_file, run_shell_command, run_tests
from .web_tools import WebSearchTool, WebReaderTool
from .ide import open_file, save_file
from .notes import add_note, list_notes
from .github import create_issue
from .fs_safety import ensure_path_is_allowed, safe_read, safe_write

__all__ = [
    "RepositoryIndexer",
    "read_file",
    "write_file",
    "run_shell_command",
    "run_tests",
    "WebSearchTool",
    "WebReaderTool",
    "open_file",
    "save_file",
    "add_note",
    "list_notes",
    "create_issue",
    "ensure_path_is_allowed",
    "safe_read",
    "safe_write",
]
