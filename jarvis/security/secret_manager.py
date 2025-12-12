from __future__ import annotations
from typing import Any, Dict

_secrets_store: Dict[str, Any] = {}

def set_secret(key: str, value: str) -> bool:
    _secrets_store[key] = value
    return True

def get_secret(key: str, default: Any = None) -> Any:
    return _secrets_store.get(key, default)
