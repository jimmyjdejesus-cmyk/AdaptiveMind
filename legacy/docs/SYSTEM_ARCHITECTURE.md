# J.A.R.V.I.S. System Architecture

This document provides a high-level overview of the J.A.R.V.I.S. platform's microservices architecture. The entire system is orchestrated via `docker-compose.yml` and is designed to be modular, scalable, and privacy-focused.

## System Diagram

```
+----------------+      +---------------------+      +-----------------+
|                |----->|                     |----->|                 |
|  API Service   |<---- |   Orchestrator      |----->|   LLM Service   |
|     (v2)       |      | (LangGraph Engine)  |      |    (Ollama)     |
|                |----->|                     |----->|                 |
+----------------+      +----------+----------+      +-----------------+
                            |      ^
                            |      |
                            v      |
                  +---------+-----------+
                  |                     |
                  |   Data Services     |
                  |                     |
                  +--+---------------+--+
                     |               |
         +-----------+-----------+   |
         |                       |   |
+--------+--------+     +--------+---+----+     +-----------------+
|                 |     |                 |     |                 |
|  Vector DB      |     |  Graph DB       |     |  Memory Service |
|   (Qdrant)      |     |   (Neo4j)       |     |    (Redis)      |
| (for RAG)       |     | (World Model)   |     | (for Cache)     |
|                 |     |                 |     |                 |
+-----------------+     +-----------------+     +-----------------+
```

## Service Components

### 1. API Service (`api`)

*   **Technology:** FastAPI (`v2/run.py`)
*   **Role:** The primary public-facing entry point for the J.A.R.V.I.S. platform. It exposes a RESTful API for clients (like the Desktop Application or other applications) to interact with the system. It handles incoming requests, authentication, and forwards tasks to the Orchestrator.

### 2. Orchestrator (`orchestrator`)

*   **Technology:** FastAPI, LangGraph (`jarvis/orchestration/server.py`)
*   **Role:** The brain of the system. The Orchestrator receives tasks from the API service and manages the entire agentic workflow. It uses LangGraph to define and execute complex graphs of operations, coordinating different agent teams, tools, and data sources to accomplish a given goal. It is responsible for breaking down tasks, routing them to the appropriate agents, and managing the state of the workflow.

### 3. LLM Service (`ollama`)

*   **Technology:** Ollama
*   **Role:** Provides access to local, self-hosted Large Language Models (LLMs). By running models locally, the platform ensures data privacy and avoids reliance on external API providers. The Orchestrator communicates with this service to get completions from the underlying language models.

### 4. Vector DB (`vector-db`)

*   **Technology:** Qdrant
*   **Role:** Serves as the long-term memory for the agents, primarily for Retrieval-Augmented Generation (RAG). Text, documents, and conversation history are converted into vector embeddings and stored here. This allows agents to perform fast, semantic searches over a large body of knowledge to inform their responses.

### 5. Graph DB (`neo4j`)

*   **Technology:** Neo4j
*   **Role:** Hosts the system's "World Model." It stores information as a knowledge graph, representing entities (people, places, concepts) and their relationships. This allows agents to reason about complex connections and maintain a structured understanding of the world, which is crucial for more advanced planning and analysis tasks.

### 6. Memory Service (`memory-service`)

*   **Technology:** Redis
*   **Role:** Acts as a high-speed, short-term memory and caching layer. It is used for storing session information, caching frequently accessed data, and as a message bus for real-time communication between different components of the system. This reduces latency and offloads work from the persistent databases.

## Data and Workflow Flow

1.  A user sends a request to the **API Service**.
2.  The API Service validates the request and forwards it to the **Orchestrator**.
3.  The **Orchestrator** creates a new workflow graph. To execute the task, it might:
    *   Query the **LLM Service** for reasoning or text generation.
    *   Fetch relevant documents from the **Vector DB** to provide context (RAG).
    *   Query the **Graph DB** to understand relationships between entities.
    *   Use the **Memory Service** to cache intermediate results.
4.  The results are passed back through the chain, and the **API Service** returns the final response to the user.
