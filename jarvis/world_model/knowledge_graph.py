from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List
import ast


@dataclass
class KnowledgeGraph:
    """Minimal knowledge graph mapping files to their functions."""

    files: Dict[str, Dict[str, List[str]]] = field(default_factory=dict)

    def add_file(self, path: str, functions: List[str] | None = None) -> None:
        """Register a file and its functions in the graph."""
        self.files[path] = {"functions": functions or []}

    def populate_from_indexer(self, indexer: "RepositoryIndexer") -> None:
        """Populate graph using a RepositoryIndexer scan of the repo."""
        repo_path = Path(indexer.repo_path)
        for py_file in repo_path.rglob("*.py"):
            try:
                source = py_file.read_text(encoding="utf-8")
                tree = ast.parse(source)
                funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                rel_path = str(py_file.relative_to(repo_path))
                self.add_file(rel_path, funcs)
            except Exception:
                continue


__all__ = ["KnowledgeGraph"]
