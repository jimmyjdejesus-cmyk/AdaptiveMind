from __future__ import annotations

import json
from typing import List, Optional

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field

from .app import JarvisApplication
from .config import AppConfig
from .logger import get_logger

logger = get_logger(__name__)


class Message(BaseModel):
    role: str = Field(..., description="Role of the speaker")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    messages: List[Message]
    persona: str = Field("generalist", description="Persona to route the request")
    temperature: float = 0.7
    max_tokens: int = Field(512, ge=32, le=4096)
    metadata: Optional[dict] = None
    external_context: Optional[List[str]] = None


class ChatResponse(BaseModel):
    content: str
    model: str
    tokens: int
    diagnostics: dict


class HealthResponse(BaseModel):
    status: str
    available_models: List[str]


class MetricsResponse(BaseModel):
    history: List[dict]


class TracesResponse(BaseModel):
    traces: List[dict]


def build_app(config: Optional[AppConfig] = None) -> FastAPI:
    jarvis_app = JarvisApplication(config=config)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        try:
            yield
        finally:
            jarvis_app.shutdown()

    fastapi_app = FastAPI(title="Jarvis Local Assistant", version="1.0.0", lifespan=lifespan)

    def _verify_api_key(request: Request) -> None:
        if not jarvis_app.config.security.api_keys:
            return
        header_key = request.headers.get("X-API-Key")
        query_key = request.query_params.get("api_key")
        provided = header_key or query_key
        if not provided or provided not in jarvis_app.config.security.api_keys:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    def _app_dependency(request: Request) -> JarvisApplication:
        _verify_api_key(request)
        return jarvis_app

    @fastapi_app.get("/health", response_model=HealthResponse)
    def health(app: JarvisApplication = Depends(_app_dependency)) -> HealthResponse:
        models = app.models()
        status_value = "ok" if models else "degraded"
        return HealthResponse(status=status_value, available_models=models)

    @fastapi_app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return _OLLAMA_UI_HTML

    @fastapi_app.get("/api/v1/models", response_model=List[str])
    def models(app: JarvisApplication = Depends(_app_dependency)) -> List[str]:
        return app.models()

    @fastapi_app.get("/api/v1/personas", response_model=List[dict])
    def personas(app: JarvisApplication = Depends(_app_dependency)) -> List[dict]:
        return app.personas()

    @fastapi_app.post("/api/v1/chat", response_model=ChatResponse)
    def chat(request: ChatRequest, app: JarvisApplication = Depends(_app_dependency)) -> ChatResponse:
        payload = app.chat(
            persona=request.persona,
            messages=[message.model_dump() for message in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            metadata=request.metadata,
            external_context=request.external_context,
        )
        return ChatResponse(**payload)

    @fastapi_app.post("/v1/chat/completions")
    async def openai_chat_completions(request: Request, app: JarvisApplication = Depends(_app_dependency)):
        """OpenAI-compatible endpoint for chat completions."""
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON")

        # Extract standard OpenAI fields
        messages = body.get("messages", [])
        model = body.get("model", "default")
        temperature = body.get("temperature", 0.7)
        max_tokens = body.get("max_tokens", 512)
        stream = body.get("stream", False)
        
        # Map to Jarvis internal format
        # Use 'generalist' persona by default, or infer from model name if possible
        persona = "generalist"
        
        if stream:
            # Streaming response
            def generate():
                try:
                    for chunk in app.stream_chat(
                        persona=persona,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        metadata={"source": "openai-api", "requested_model": model}
                    ):
                        # Yield OpenAI-compatible SSE format
                        delta = {"content": chunk["content"]} if chunk["content"] else {}
                        if chunk["finished"]:
                            delta["finish_reason"] = "stop"
                        event = {
                            "id": "chatcmpl-jarvis-stream",
                            "object": "chat.completion.chunk",
                            "created": 0,  # TODO: Add timestamp
                            "model": chunk["model"],
                            "choices": [
                                {
                                    "index": 0,
                                    "delta": delta,
                                    "finish_reason": "stop" if chunk["finished"] else None,
                                }
                            ],
                        }
                        yield f"data: {json.dumps(event)}\n\n"
                        if chunk["finished"]:
                            yield "data: [DONE]\n\n"
                            break
                except Exception as e:
                    logger.error(f"Streaming chat completion failed: {e}")
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
            return StreamingResponse(generate(), media_type="text/plain")
        else:
            # Non-streaming response
            try:
                payload = app.chat(
                    persona=persona,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    metadata={"source": "openai-api", "requested_model": model}
                )
                
                # Transform response to OpenAI format
                return {
                    "id": "chatcmpl-jarvis",
                    "object": "chat.completion",
                    "created": 0, # TODO: Add timestamp
                    "model": payload["model"],
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": payload["content"]
                            },
                            "finish_reason": "stop"
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 0, # TODO: Calculate
                        "completion_tokens": payload["tokens"],
                        "total_tokens": payload["tokens"]
                    }
                }
            except Exception as e:
                logger.error(f"Chat completion failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    @fastapi_app.get("/api/v1/monitoring/metrics", response_model=MetricsResponse)
    def metrics(app: JarvisApplication = Depends(_app_dependency)) -> MetricsResponse:
        return MetricsResponse(history=app.metrics_snapshot())

    @fastapi_app.get("/api/v1/monitoring/traces", response_model=TracesResponse)
    def traces(app: JarvisApplication = Depends(_app_dependency)) -> TracesResponse:
        return TracesResponse(traces=app.traces_latest())

    return fastapi_app


_OLLAMA_UI_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Jarvis Ollama Console</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; background: #111; color: #f5f5f5; }
        h1 { color: #00e0ff; }
        .container { max-width: 720px; margin: auto; }
        textarea { width: 100%; height: 160px; padding: 1rem; background: #1b1b1b; color: #f5f5f5; border: 1px solid #333; border-radius: 8px; }
        select, button { padding: 0.5rem; margin-top: 0.5rem; background: #00e0ff; color: #111; border: none; border-radius: 6px; cursor: pointer; }
        pre { white-space: pre-wrap; background: #1b1b1b; padding: 1rem; border-radius: 8px; border: 1px solid #333; }
        label { display: block; margin-top: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Jarvis Ollama Console</h1>
        <p>Local-first assistant with deep research, persona routing, and secure API key gating.</p>
        <label for="persona">Persona</label>
        <select id="persona"></select>
        <label for="prompt">Prompt</label>
        <textarea id="prompt" placeholder="Ask Jarvis anything..."></textarea>
        <button onclick="sendChat()">Send</button>
        <pre id="output">Response will appear here.</pre>
    </div>
    <script>
        async function loadPersonas() {
            const response = await fetch('/api/v1/personas');
            const personas = await response.json();
            const select = document.getElementById('persona');
            personas.forEach(p => {
                const option = document.createElement('option');
                option.value = p.name;
                option.textContent = `${p.name} — ${p.description}`;
                select.appendChild(option);
            });
        }
        async function sendChat() {
            const prompt = document.getElementById('prompt').value;
            const persona = document.getElementById('persona').value || 'generalist';
            const body = {
                persona,
                messages: [
                    { role: 'user', content: prompt }
                ],
                metadata: { objective: 'ui-chat' }
            };
            const response = await fetch('/api/v1/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            if (!response.ok) {
                document.getElementById('output').textContent = 'Request failed: ' + response.status;
                return;
            }
            const data = await response.json();
            document.getElementById('output').textContent = data.content + '\n\nTokens: ' + data.tokens + '\nModel: ' + data.model;
        }
        loadPersonas();
    </script>
</body>
</html>
"""


__all__ = ["build_app"]

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("JARVIS_PORT", 8000))
    host = os.getenv("JARVIS_HOST", "0.0.0.0")
    
    # Initialize config
    from .config import load_config
    config = load_config()
    
    app = build_app(config)
    
    uvicorn.run(app, host=host, port=port)
