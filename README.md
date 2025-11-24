# Jarvis Local Assistant Runtime

Jarvis_AI is a local-first multi-persona assistant that prioritises verifiable truth, observability, and secure extensibility. The new runtime integrates with the agent-ui frontend for a modern interface, an adaptive routing pipeline, and a comprehensive monitoring stack to support deep research workflows without sacrificing privacy.

## Key Features

- **Agent-UI Integration** – Modern frontend interface for sending prompts to the adaptive router. Integrates with agent-ui for enhanced user experience.
- **Context Engineering Pipeline** – Automatic persona prompts, conversation history, research snippets, and optional local documents with semantic chunking.
- **Adaptive Routing** – Persona-aware router selects between Ollama, WindowsML, or the contextual fallback while recording metrics and traces.
- **Security Controls** – API key enforcement and structured audit logging hooks to keep cloud usage gated.
- **Observability** – Central JSON logger, rolling metrics registry, and trace harvesting endpoints.
- **Extensibility Templates** – Ready-made templates for Model Context Protocol (MCP) and Language Server Protocol (LSP) adapters.

## Getting Started

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### Running the API & UI

```bash
uvicorn jarvis_core.server:build_app --factory --host 127.0.0.1 --port 8000
```

The backend automatically attempts to use a local Ollama instance (`OLLAMA_HOST`) and falls back to the contextual generator when unavailable. To enable WindowsML acceleration, set `JARVIS_CONFIG` to a JSON file that provides the ONNX model path on Windows.

### Configuration
### Frontend Integration

For the user interface, use [agent-ui](https://github.com/jimmyjdejesus-cmyk/agent-ui), a modern frontend that connects to this Jarvis_AI backend.

To set up:

1. Clone agent-ui: `git clone https://github.com/jimmyjdejesus-cmyk/agent-ui.git`
2. Follow agent-ui setup instructions.
3. Configure agent-ui to point to Jarvis_AI backend at `http://127.0.0.1:8000`


### Frontend Integration

For the user interface, use [agent-ui](https://github.com/jimmyjdejesus-cmyk/agent-ui), a modern frontend that connects to this Jarvis_AI backend.

To set up:

1. Clone agent-ui: `git clone https://github.com/jimmyjdejesus-cmyk/agent-ui.git`
2. Follow agent-ui setup instructions.
3. Configure agent-ui to point to Jarvis_AI backend at `http://127.0.0.1:8000`


