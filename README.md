# Jarvis AI - Advanced Multi-Agent System

Jarvis_AI is a comprehensive, local-first multi-persona assistant that prioritises verifiable truth, observability, and secure extensibility. The system integrates modern agent architectures with legacy compatibility for a seamless development experience.

## Key Features

### Modern Architecture
- **Meta-Agent Orchestration** – Central coordinator managing multiple specialist LLMs
- **Agent-UI Integration** – Modern frontend interface for sending prompts to the adaptive router
- **Context Engineering Pipeline** – Automatic persona prompts, conversation history, research snippets, and optional local documents with semantic chunking
- **Adaptive Routing** – Persona-aware router selects between Ollama, WindowsML, or the contextual fallback while recording metrics and traces

### Legacy Compatibility  
- **Legacy Module Support** – Maintains compatibility with existing jarvis/legacy architecture
- **Migration Path** – Gradual transition from legacy to modern Jarvis_Local components
- **Backward Compatibility** – Existing agents and workflows continue to function

### Security & Observability
- **Security Controls** – API key enforcement and structured audit logging hooks to keep cloud usage gated
- **Observability** – Central JSON logger, rolling metrics registry, and trace harvesting endpoints
- **Extensibility Templates** – Ready-made templates for Model Context Protocol (MCP) and Language Server Protocol (LSP) adapters

## Getting Started

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the API & UI

```bash
# Modern Jarvis_Local system
python Jarvis_Local/main.py

# Or legacy jarvis system  
python legacy/jarvis/__main__.py

# FastAPI backend (for agent-ui frontend)
uvicorn jarvis_core.server:build_app --factory --host 127.0.0.1 --port 8000
```

The backend automatically attempts to use a local Ollama instance (`OLLAMA_HOST`) and falls back to the contextual generator when unavailable. To enable WindowsML acceleration, set `JARVIS_CONFIG` to a JSON file that provides the ONNX model path on Windows.

### Configuration

The system supports multiple configuration approaches:

1. **Environment Variables** - Set `JARVIS_CONFIG` or use `.env` files
2. **Modern Configuration** - Use `Jarvis_Local/config.py` and `Jarvis_Local/settings.py`
3. **Legacy Configuration** - Maintain existing legacy configuration patterns

### Frontend Integration

For the user interface, use [agent-ui](https://github.com/jimmyjdejesus-cmyk/agent-ui), a modern frontend that connects to this Jarvis_AI backend.

To set up:

1. Clone agent-ui: `git clone https://github.com/jimmyjdejesus-cmyk/agent-ui.git`
2. Follow agent-ui setup instructions.
3. Configure agent-ui to point to Jarvis_AI backend at `http://127.0.0.1:8000`

## Architecture Overview

### Modern Components (Jarvis_Local/)
- **Agents** – Base, meta, and specialist agent implementations
- **Tools** – Utility modules for various operations
- **UI** – Component-based interface system
- **Orchestrator** – Central coordination and message routing

### Legacy Components (legacy/)
- **jarvis/** – Original jarvis implementation
- **agent/** – Legacy agent system
- **orchestration/** – Original orchestration mechanisms

### Core Services (jarvis_core/)
- **FastAPI backend** for modern API endpoints
- **Configuration management** with pydantic models
- **LLM integration** with Ollama, OpenRouter, and WindowsML
- **Monitoring and observability** infrastructure

## Migration Strategy

The system supports both legacy and modern architectures simultaneously, allowing for gradual migration:

1. **Phase 1** – Dual operation (legacy + modern)
2. **Phase 2** – Gradual component migration
3. **Phase 3** – Legacy deprecation (when ready)

## Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run type checking
python -m mypy jarvis_core/

# Run linting
python -m flake8 jarvis_core/
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `python -m pytest tests/`
5. Submit a pull request

For detailed development guidelines, see the documentation in `docs/`.
