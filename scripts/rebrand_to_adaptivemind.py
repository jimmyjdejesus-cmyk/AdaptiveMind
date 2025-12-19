#!/usr/bin/env python3
"""# Copyright (c) 2025 Jimmy De Jesus (Bravetto).

# Licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0).
# See https://creativecommons.org/licenses/by/4.0/ for license terms.

Rebrand Jarvis to AdaptiveMind across the codebase.
Preserves compatibility shims and handles special cases.
"""
import re
from pathlib import Path

# Directories to exclude from rebranding
EXCLUDE_DIRS = {
    ".git", ".venv", ".venv-1", "venv", "env", "__pycache__",
    "node_modules", ".pytest_cache", "agent_scaling_laws"
}

# Files to exclude
EXCLUDE_FILES = {
    "Jarvis_Local/__init__.py",  # Compatibility shim
}

# Replacement mappings (order matters!)
REPLACEMENTS: list[tuple[str, str]] = [
    # Class names
    (r'\bJarvisApplication\b', 'AdaptiveMindApplication'),
    (r'\bJarvisBackend\b', 'AdaptiveMindBackend'),
    (r'\bJarvisHandler\b', 'AdaptiveMindHandler'),
    (r'\bJarvisDemoHandler\b', 'AdaptiveMindDemoHandler'),
    (r'\bMCPJarvisAgent\b', 'MCPAdaptiveMindAgent'),

    # Environment variables
    (r'\bJARVIS_([A-Z_]+)\b', r'ADAPTIVEMIND_\1'),

    # File paths and config
    (r'\.adaptivemind/', '.adaptivemind/'),
    (r'~/.adaptivemind', '~/.adaptivemind'),
    (r'jarvis_config\.json', 'adaptivemind_config.json'),
    (r'jarvis_local\.log', 'adaptivemind_local.log'),
    (r'jarvis\.log', 'adaptivemind.log'),

    # API/Service names
    (r'"adaptivemind-default"', '"adaptivemind-default"'),
    (r'"adaptivemind-local"', '"adaptivemind-local"'),
    (r'"owned_by": "adaptivemind"', '"owned_by": "adaptivemind"'),
    (r'"adaptivemind_local_ai"', '"adaptivemind_local_ai"'),

    # UI/Display text
    (r'AdaptiveMind Local Assistant', 'AdaptiveMind Local Assistant'),
    (r'AdaptiveMind Ollama Console', 'AdaptiveMind Ollama Console'),
    (r'AdaptiveMind AI', 'AdaptiveMind AI'),
    (r'AdaptiveMind Working Demo', 'AdaptiveMind Working Demo'),
    (r'AdaptiveMind Local', 'AdaptiveMind Local'),
    (r'Ask AdaptiveMind', 'Ask AdaptiveMind'),
    (r'AdaptiveMind is thinking', 'AdaptiveMind is thinking'),
    (r'You are AdaptiveMind,', 'You are AdaptiveMind,'),

    # Email/URLs (if any - these would need manual review)
    (r'support@jarvis\.ai', 'support@adaptivemind.ai'),
    (r'api\.jarvis\.ai', 'api.adaptivemind.ai'),

    # Documentation
    (r'AdaptiveMind Framework', 'AdaptiveMind Framework'),
    (r'AdaptiveMind system', 'AdaptiveMind system'),
    (r'AdaptiveMind framework', 'AdaptiveMind framework'),

    # Generic mentions (be careful with these)
    (r'Starting AdaptiveMind', 'Starting AdaptiveMind'),
    (r'initialize AdaptiveMind', 'initialize AdaptiveMind'),
    (r'AdaptiveMind app', 'AdaptiveMind app'),
    (r'AdaptiveMind runtime', 'AdaptiveMind runtime'),
]

def should_process(path: Path) -> bool:
    """Check if file should be processed."""
    if not path.is_file():
        return False

    # Check excluded directories
    if any(exc in path.parts for exc in EXCLUDE_DIRS):
        return False

    # Check excluded files
    rel_path = str(path.relative_to(Path.cwd()))
    if rel_path in EXCLUDE_FILES:
        return False

    # Only process text files
    return path.suffix not in {'.pyc', '.png', '.jpg', '.jpeg', '.gif', '.zip', '.tar', '.ico'}

def apply_replacements(content: str) -> tuple[str, int]:
    """Apply all replacements to content. Returns (new_content, count)."""
    count = 0
    new_content = content

    for pattern, replacement in REPLACEMENTS:
        new_content, n = re.subn(pattern, replacement, new_content)
        count += n

    return new_content, count

def rebrand_file(path: Path) -> bool:
    """Rebrand a single file. Returns True if modified."""
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            original = f.read()

        new_content, count = apply_replacements(original)

        if count > 0:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True

        return False
    except Exception:
        return False

def main():
    """Main rebranding function."""
    root = Path.cwd()
    files_modified = 0
    total_replacements = 0


    # Process all files
    for path in root.rglob('*'):
        if should_process(path):
            try:
                with open(path, encoding='utf-8', errors='ignore') as f:
                    original = f.read()

                new_content, count = apply_replacements(original)

                if count > 0:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    files_modified += 1
                    total_replacements += count
            except Exception:
                pass


if __name__ == "__main__":
    main()
