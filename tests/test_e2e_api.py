import os
import time
import json
import asyncio
import pytest
import requests

BASE_URL = os.getenv("JARVIS_TEST_BASE_URL", "http://127.0.0.1:8000")
REQUIRE_NEW_RUNTIME = os.getenv("REQUIRE_NEW_RUNTIME", "false").lower() in {"1", "true", "yes", "on"}


def wait_for_health(timeout: int = 25):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{BASE_URL}/health", timeout=5)
            if r.status_code == 200 and r.json().get("status") == "ok":
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def _assert_status(resp: requests.Response):
    if REQUIRE_NEW_RUNTIME:
        assert resp.status_code == 200, f"Expected 200 with REQUIRE_NEW_RUNTIME, got {resp.status_code}"
    else:
        assert resp.status_code in (200, 503), f"Unexpected status code: {resp.status_code}"


def test_health():
    assert wait_for_health(), "Backend health endpoint not responding with status ok"


def test_models_endpoint():
    r = requests.get(f"{BASE_URL}/api/models", timeout=15)
    _assert_status(r)


@pytest.mark.timeout(60)
def test_chat_endpoint():
    payload = {"messages": [{"role": "user", "content": "Hello from pytest"}]}
    r = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=45)
    _assert_status(r)
    if r.status_code == 200:
        data = r.json()
        assert "content" in data


@pytest.mark.timeout(60)
def test_agent_execute_bridge():
    payload = {"agent_type": "research", "objective": "Short objective"}
    r = requests.post(f"{BASE_URL}/api/agents/execute", json=payload, timeout=45)
    _assert_status(r)


@pytest.mark.timeout(60)
def test_workflow_execute():
    payload = {"workflow_type": "research", "parameters": {"query": "pytest"}}
    r = requests.post(f"{BASE_URL}/api/workflows/execute", json=payload, timeout=45)
    _assert_status(r)
