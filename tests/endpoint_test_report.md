# AdaptiveMind/ Jarvis AI Endpoint Testing Report

**Test Date**: 2025-12-17 17:05:15
**Server URL**: http://localhost:8000

## Summary
- **Total Tests**: 5
- **Successful**: 3
- **Failed**: 2
- **Success Rate**: 60.0%

## Detailed Results

### Health
- **Status**: ✅ Success
- **HTTP Status**: 200
- **Description**: Health check endpoint
- **Response**: 
```json
{
  "status": "ok",
  "available_models": [
    "contextual-fallback"
  ]
}
```

### Models
- **Status**: ❌ Failed
- **HTTP Status**: 404
- **Description**: List available models
- **Response**: 
```json
{
  "error": "Not Found"
}
```

### Personas
- **Status**: ❌ Failed
- **HTTP Status**: 404
- **Description**: List configured personas
- **Response**: 
```json
{
  "error": "Not Found"
}
```

### Chat Basic
- **Status**: ✅ Success
- **HTTP Status**: 200
- **Description**: Basic chat completion
- **Response**: 
```json
{
  "content": "Persona focus: ## Persona\nMost recent user request: Hello, how are you?\nKey context terms: are, persona, you, a, research\nResponse: Based on the available local context, here is a structured summary and recommended next steps.\n- Context Window Size: 23 tokens (approx.)\n- Suggested Actions: Verify facts, consult linked research snippets, and prepare citations before responding.\n- Safety: Ensure API usage complies with configured policies and redact sensitive data.",
  "model": "contextual-fallback",
  "tokens": 70,
  "diagnostics": {}
}
```

### Chat Complex
- **Status**: ✅ Success
- **HTTP Status**: 200
- **Description**: Complex chat with context
- **Response**: 
```json
{
  "content": "Persona focus: ## Persona\nMost recent user request: Tell me more about it.\nKey context terms: is, the, capital, of, persona\nResponse: Based on the available local context, here is a structured summary and recommended next steps.\n- Context Window Size: 38 tokens (approx.)\n- Suggested Actions: Verify facts, consult linked research snippets, and prepare citations before responding.\n- Safety: Ensure API usage complies with configured policies and redact sensitive data.",
  "model": "contextual-fallback",
  "tokens": 71,
  "diagnostics": {}
}
```

