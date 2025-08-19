# Jarvis AI V2

## Overview

Jarvis AI V2 is a next-generation AI assistant built on the Lang family of frameworks:

- **LangChain** for tool integration
- **LangGraph** for workflow management
- **LangGraphUI** for visualization

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the system:
```bash
python run.py
```

## Architecture

The V2 architecture follows a node-based workflow system:

- **Planner**: Analyzes tasks and creates execution plans
- **Executor**: Carries out actions using specialized tools
- **Critic**: Evaluates results and suggests improvements

## Features

- Advanced reasoning with multi-step planning
- Tool integration with standardized interfaces
- Visualization of agent thought processes
- Fallback mechanisms for robustness
