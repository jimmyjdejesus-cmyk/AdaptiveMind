# J.A.R.V.I.S. - A Modular Agentic Platform

J.A.R.V.I.S. is a powerful, privacy-first, and modular platform for developing and orchestrating advanced AI agents. It is designed with a microservices architecture to be scalable, extensible, and robust.

## Core Architecture

The platform is composed of several interconnected services that work together to provide a comprehensive environment for agentic workflows. The entire system is orchestrated using Docker Compose.

### Key Services:

*   **API (`v2`):** The main entry point for interacting with the J.A.R.V.I.S. platform.
*   **Orchestrator:** The central hub that manages agent teams, message buses, and complex workflows using LangGraph.
*   **Memory Service (Redis):** Provides a high-speed cache for session data and short-term agent memory.
*   **Vector DB (Qdrant):** A vector database for enabling Retrieval-Augmented Generation (RAG), giving agents long-term, searchable knowledge.
*   **Graph DB (Neo4j):** A graph database used for building and managing a sophisticated world model and knowledge graphs.
*   **LLM Service (Ollama):** Integrates with Ollama to run local, open-source language models, ensuring privacy and control.

For a more detailed explanation of the system's design, please see the [System Architecture document](./docs/SYSTEM_ARCHITECTURE.md).

## Getting Started (Recommended)

The easiest way to run the entire J.A.R.V.I.S. platform is with Docker and Docker Compose.

### Prerequisites

*   Docker
*   Docker Compose

### Running the Platform

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jimmyjdejesus-cmyk/Jarvis_AI.git
    cd Jarvis_AI
    ```

2.  **Set up environment variables:**
    Create a `.env` file by copying the example file and customize it as needed.
    ```bash
    cp .env.example .env
    ```

3.  **Launch the services:**
    ```bash
    docker-compose up -d --build
    ```

This command will build the container images and start all the necessary services in the background. You can now interact with the J.A.R.V.I.S. API, which will be available at `http://localhost:8000`.

---

## J.A.R.V.I.S. Desktop Application (Work in Progress)

In addition to the core platform, a new desktop application is under development to provide a rich graphical user interface for interacting with J.A.R.V.I.S.

**Note:** This application is in a very early, pre-alpha stage. The backend is currently mocked and is **not yet integrated** with the core J.A.R.V.I.S. platform.

### Architecture

*   **Backend:** A Python application using **FastAPI** and **WebSockets**. Source is in the `app/` directory.
*   **Frontend:** A **React** single-page application. Source is in the `src-tauri/src/` directory.
*   **Desktop Shell:** **Tauri** is used to wrap the frontend and backend into a single, cross-platform desktop executable.

### Development Setup

To run the desktop app in a development environment, you will need **Python 3.8+** and **Node.js**.

1.  **Install all dependencies:**
    The consolidated `requirements.txt` in the root includes all necessary Python packages.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Install frontend dependencies:**
    ```bash
    cd src-tauri
    npm install
    cd ..
    ```

3.  **Run the development servers:**
    You will need two terminals.

    *   **Terminal 1 (Backend):** `python app/main.py`
    *   **Terminal 2 (Frontend):** `cd src-tauri && npm run dev`

This will open a native window with the prototype UI running.
