"""Shared memory FastAPI service with scoped access."""

from __future__ import annotations

import hashlib
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from .vector_store import add_text

app = FastAPI(title="SharedMemoryService")

# Nested dictionary principal -> scope -> key -> value
_memory: Dict[str, Dict[str, Dict[str, str]]] = {}
# Collected WS7 events for test inspection
EVENTS: List[Dict[str, str]] = []

# List of sensitive values that must be masked in events
SENSITIVE_VALUES: List[str] = []
SECRET_MASK = "***"


class MemoryItem(BaseModel):
    """Item stored in shared memory."""

    key: str
    value: str


def _mask(value: str) -> str:
    """Mask any sensitive substrings in ``value``."""
    for secret in SENSITIVE_VALUES:
        value = value.replace(secret, SECRET_MASK)
    return value


def _emit(event_type: str, principal: str, scope: str, key: Optional[str] = None) -> None:
    """Record an event following the WS7 structure, masking secrets."""
    event = {
        "version": "WS7",
        "type": _mask(event_type),
        "principal": _mask(principal),
        "scope": _mask(scope),
    }
    if key is not None:
        event["key"] = _mask(key)
    EVENTS.append(event)


def _verify_principal(request: Request, principal: str) -> None:
    """Ensure the caller principal matches the target principal."""
    caller = request.headers.get("X-Principal")
    if caller != principal:
        raise HTTPException(status_code=403, detail="Forbidden")


@app.post("/{principal}/{scope}")
def write_item(principal: str, scope: str, item: MemoryItem, request: Request) -> Dict[str, str]:
    """Write a key/value pair within a principal's scope."""
    _verify_principal(request, principal)
    store = _memory.setdefault(principal, {}).setdefault(scope, {})
    store[item.key] = item.value
    # Persist text to vector store for semantic retrieval
    add_text(principal, scope, item.key, item.value)
    _emit("write", principal, scope, item.key)
    return {"status": "ok"}


@app.get("/{principal}/{scope}/hash")
def scope_hash(principal: str, scope: str, request: Request) -> Dict[str, str]:
    """Return a SHA256 hash of all entries in a scope."""
    _verify_principal(request, principal)
    scope_data = _memory.get(principal, {}).get(scope)
    if scope_data is None:
        raise HTTPException(status_code=404, detail="Not found")
    hasher = hashlib.sha256()
    for k in sorted(scope_data):
        hasher.update(k.encode("utf-8"))
        hasher.update(scope_data[k].encode("utf-8"))
    digest = hasher.hexdigest()
    _emit("hash", principal, scope)
    return {"hash": digest}


@app.get("/{principal}/{scope}/{key}")
def read_item(principal: str, scope: str, key: str, request: Request) -> Dict[str, str]:
    """Read a value from scoped memory."""
    _verify_principal(request, principal)
    try:
        value = _memory[principal][scope][key]
    except KeyError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=404, detail="Not found") from exc
    _emit("read", principal, scope, key)
    return {"value": value}
