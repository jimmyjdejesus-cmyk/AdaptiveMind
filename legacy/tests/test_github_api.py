import os
import sys
import types
import requests
import pytest

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root)

# Stub missing modules required by legacy.agent.tools
agent_module = types.ModuleType("agent")
features_module = types.ModuleType("features")
setattr(agent_module, "features", features_module)
sys.modules["agent"] = agent_module
sys.modules["agent.features"] = features_module

for name in [
    "file_ingest",
    "browser_automation",
    "image_generation",
    "rag_handler",
    "code_review",
    "code_search",
    "repo_context",
]:
    mod = types.ModuleType(name)
    setattr(features_module, name, mod)
    sys.modules[f"agent.features.{name}"] = mod

tools_module = types.ModuleType("tools")
code_intelligence_module = types.ModuleType("code_intelligence")
code_intelligence_module.engine = types.SimpleNamespace(
    get_code_completion=lambda *a, **k: None,
    record_completion_feedback=lambda *a, **k: None,
)
setattr(tools_module, "code_intelligence", code_intelligence_module)
sys.modules["tools"] = tools_module
sys.modules["tools.code_intelligence"] = code_intelligence_module

from legacy.agent.tools import run_tool


class MockResponse:
    def __init__(self, status_code=200, json_data=None, headers=None, text=""):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.headers = headers or {}
        self.text = text

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


def test_open_issue(monkeypatch):
    def mock_post(url, json, headers, timeout):
        assert "repos/owner/repo/issues" in url
        return MockResponse(status_code=201, json_data={"id": 1, "title": json["title"]})

    monkeypatch.setattr(requests, "post", mock_post)

    step = {
        "tool": "github_api",
        "args": {
            "action": "open_issue",
            "repo": "owner/repo",
            "title": "Bug report",
            "body": "Details",
            "token": "t",
        },
    }
    result = run_tool(step)
    assert result["title"] == "Bug report"


def test_create_pull_request(monkeypatch):
    def mock_post(url, json, headers, timeout):
        assert "repos/owner/repo/pulls" in url
        return MockResponse(status_code=201, json_data={"id": 2, "title": json["title"]})

    monkeypatch.setattr(requests, "post", mock_post)

    step = {
        "tool": "github_api",
        "args": {
            "action": "create_pull_request",
            "repo": "owner/repo",
            "title": "PR title",
            "head": "feature",
            "base": "main",
            "body": "Description",
            "token": "t",
        },
    }
    result = run_tool(step)
    assert result["title"] == "PR title"


def test_rate_limit(monkeypatch):
    def mock_post(url, json, headers, timeout):
        headers = {"X-RateLimit-Remaining": "0"}
        return MockResponse(status_code=403, headers=headers, text="rate limit exceeded")

    monkeypatch.setattr(requests, "post", mock_post)

    step = {
        "tool": "github_api",
        "args": {
            "action": "open_issue",
            "repo": "owner/repo",
            "title": "Bug",
            "token": "t",
        },
    }
    result = run_tool(step)
    assert result["error"] == "GitHub API rate limit exceeded"


def test_missing_fields():
    step = {"tool": "github_api", "args": {"action": "open_issue", "repo": "owner/repo", "token": "t"}}
    with pytest.raises(ValueError):
        run_tool(step)
