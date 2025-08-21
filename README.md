# Jarvis AI
[![CI](https://github.com/jimmyjdejesus-cmyk/Jarvis_AI/actions/workflows/ci.yml/badge.svg)](https://github.com/jimmyjdejesus-cmyk/Jarvis_AI/actions/workflows/ci.yml)

A privacy-first, modular AI development assistant with a unified, configurable architecture.

## 🚀 Quick Start

### Install from PyPI

```bash
pip install jarvis-ai
jarvis run
```

### Docker

```bash
docker compose up -d
```

## 🏛️ Architecture

The Jarvis AI project has been refactored to use a single, unified `JarvisAgent`. This agent consolidates all the capabilities of the previous agents into a single, configurable class. You can get an instance of the agent with different capabilities using the following convenience functions:

```python
import jarvis

# Get a simple agent with basic chat functionality
simple_agent = jarvis.get_simple_jarvis()

# Get a "smart" agent with multi-model routing (MCP)
smart_agent = jarvis.get_smart_jarvis()

# Get a "super" agent with multi-agent orchestration
super_agent = jarvis.get_super_jarvis()

# Get the "ultimate" agent with all features, including workflows
ultimate_agent = jarvis.get_ultimate_jarvis()
```

You can also create a custom agent configuration by calling `get_jarvis_agent` directly:

```python
import jarvis

my_agent = jarvis.get_jarvis_agent(
    enable_mcp=True,
    enable_multi_agent=False,
    enable_workflows=True
)
```

## 📋 Features

- **Unified Agent:** A single, configurable agent that can be adapted to different use cases.
- **Dynamic Orchestration:** Uses a `DynamicOrchestrator` powered by `langgraph` to coordinate specialist agents.
- **Multi-Model Routing (MCP):** Can route requests to the best model for the job.
- **Specialist Agents:** A suite of specialist agents for tasks like code review, security analysis, and more.
- **Workflow Automation:** Can execute complex, multi-step workflows.

## 🔧 Development

```bash
git clone https://github.com/jimmyjdejesus-cmyk/Jarvis_AI.git
cd Jarvis_AI
pip install -e .[dev]
python -m pytest
```

Note: The test suite is currently under development. To run the tests for the new unified agent, use:
`python -m pytest tests/test_unified_agent.py`

## 📄 License

MIT
