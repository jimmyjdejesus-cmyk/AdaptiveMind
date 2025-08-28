"""Minimal FastAPI application exposing knowledge graph endpoints."""

from fastapi import FastAPI, HTTPException, Query

from .knowledge_graph import knowledge_graph

app = FastAPI()


@app.get("/knowledge/query")
def get_knowledge_query(
    q: str = Query(..., description="Node search"),
) -> dict:
    """Return results from the knowledge graph for the given query."""
    try:
        results = knowledge_graph.query(q)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"results": results}


@app.get("/health")
def get_health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
