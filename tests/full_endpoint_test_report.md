# AdaptiveMind/ Jarvis AI Full Endpoint Testing Report

**Test Date**: 2025-12-18 10:50:15
**Server URL**: http://localhost:8000
**OpenAPI Specification**: Complete endpoint coverage

## Summary
- **Total Tests**: 21
- **Successful**: 17
- **Failed**: 4
- **Success Rate**: 81.0%

## Health & Status
- **Health**: ✅
  - Response Preview: `{'status': 'ok', 'available_models': ['ollama', 'contextual-fallback']}`
  - **Category Success Rate**: 100.0%

## Core API
- **Models**: ✅
  - Response Preview: `['ollama', 'contextual-fallback']`
- **Personas**: ✅
  - Response Preview: `[{'name': 'generalist', 'description': 'Balanced assistant persona', 'max_context_window': 4096, 'ro...`
- **Chat Basic**: ❌
- **Chat Complex**: ❌
  - **Category Success Rate**: 50.0%

## Monitoring
- **Monitoring Metrics**: ✅
  - Response Preview: `{'history': [{'request_count': 0, 'average_latency_ms': 0.0, 'max_latency_ms': 0.0, 'tokens_generate...`
- **Monitoring Traces**: ✅
  - Response Preview: `{'traces': []}`
  - **Category Success Rate**: 100.0%

## Management - System
- **System Status**: ✅
  - Response Preview: `{'status': 'healthy', 'uptime_seconds': 51.17583107948303, 'version': '1.0.0', 'active_backends': ['...`
  - **Category Success Rate**: 100.0%

## Management - Routing
- **Routing Config Get**: ✅
  - Response Preview: `{'allowed_personas': [], 'enable_adaptive_routing': True}`
- **Routing Config Put**: ❌
  - **Category Success Rate**: 50.0%

## Management - Backends
- **Backends List**: ✅
  - Response Preview: `{'backends': [{'name': 'ollama', 'type': 'ollama', 'is_available': True, 'last_checked': 1766073015....`
- **Backend Test**: ✅
  - Response Preview: `{'success': True, 'latency_ms': 0.00095367431640625, 'error': None}`
  - **Category Success Rate**: 100.0%

## Management - Context
- **Context Config Get**: ✅
  - Response Preview: `{'extra_documents_dir': None, 'enable_semantic_chunking': True, 'max_combined_context_tokens': 8192}`
- **Context Config Put**: ✅
  - Response Preview: `{'extra_documents_dir': None, 'enable_semantic_chunking': True, 'max_combined_context_tokens': 8192}`
  - **Category Success Rate**: 100.0%

## Management - Security
- **Security Status**: ✅
  - Response Preview: `{'api_keys_count': 0, 'audit_log_enabled': False}`
  - **Category Success Rate**: 100.0%

## Management - Personas CRUD
- **Persona Create**: ✅
  - Response Preview: `{'name': 'test-persona', 'description': 'Test persona for endpoint testing', 'system_prompt': 'You a...`
- **Persona Update**: ✅
  - Response Preview: `{'name': 'test-persona', 'description': 'Updated test persona description', 'system_prompt': 'You ar...`
- **Persona Delete**: ✅
  - Response Preview: `{'message': "Persona 'test-persona' deleted successfully"}`
  - **Category Success Rate**: 100.0%

## OpenAI-Compatible
- **Openai Chat**: ❌
- **Openai Models**: ✅
  - Response Preview: `{'object': 'list', 'data': [{'id': 'llama3.2:latest', 'object': 'model', 'created': 1766073015, 'own...`
  - **Category Success Rate**: 50.0%

## Configuration
- **Config Save**: ✅
  - Response Preview: `{'success': True, 'config_hash': '62095714ce57270d', 'message': 'Configuration saved successfully (i...`
  - **Category Success Rate**: 100.0%

## Detailed Results

### Health
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /health
- **HTTP Status**: 200
- **Description**: Health check endpoint
- **Response**: 
```json
{
  "status": "ok",
  "available_models": [
    "ollama",
    "contextual-fallback"
  ]
}
```

### Models
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /api/v1/models
- **HTTP Status**: 200
- **Description**: List available models
- **Response**: 
```json
[
  "ollama",
  "contextual-fallback"
]
```

### Personas
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /api/v1/personas
- **HTTP Status**: 200
- **Description**: List configured personas
- **Response**: 
```json
[
  {
    "name": "generalist",
    "description": "Balanced assistant persona",
    "max_context_window": 4096,
    "routing_hint": "general"
  }
]
```

### Chat Basic
- **Status**: ❌ Failed
- **Method**: POST
- **Endpoint**: /api/v1/chat
- **HTTP Status**: 500
- **Description**: Basic chat completion
- **Response**: 
```json
{
  "detail": "Chat request failed"
}
```

### Chat Complex
- **Status**: ❌ Failed
- **Method**: POST
- **Endpoint**: /api/v1/chat
- **HTTP Status**: 500
- **Description**: Complex chat with context
- **Response**: 
```json
{
  "detail": "Chat request failed"
}
```

### Monitoring Metrics
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /api/v1/monitoring/metrics
- **HTTP Status**: 200
- **Description**: Get metrics history
- **Response**: 
```json
{
  "history": [
    {
      "request_count": 0,
      "average_latency_ms": 0.0,
      "max_latency_ms": 0.0,
      "tokens_generated": 0,
      "context_tokens": 0,
      "personas_used": {},
      "timestamp": 1766072994.55075
    }
  ]
}
```

### Monitoring Traces
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /api/v1/monitoring/traces
- **HTTP Status**: 200
- **Description**: Get request traces
- **Response**: 
```json
{
  "traces": []
}
```

### System Status
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /api/v1/management/system/status
- **HTTP Status**: 200
- **Description**: Get system status
- **Response**: 
```json
{
  "status": "healthy",
  "uptime_seconds": 51.17583107948303,
  "version": "1.0.0",
  "active_backends": [
    "ollama",
    "contextual-fallback"
  ],
  "active_personas": [],
  "config_hash": "7d8fda481bc6fa64"
}
```

### Routing Config Get
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /api/v1/management/routing/config
- **HTTP Status**: 200
- **Description**: Get routing configuration
- **Response**: 
```json
{
  "allowed_personas": [],
  "enable_adaptive_routing": true
}
```

### Routing Config Put
- **Status**: ❌ Failed
- **Method**: PUT
- **Endpoint**: /api/v1/management/config/routing
- **HTTP Status**: 400
- **Description**: Update routing configuration
- **Response**: 
```json
{
  "detail": "Persona 'test-persona' does not exist"
}
```

### Backends List
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /api/v1/management/backends
- **HTTP Status**: 200
- **Description**: List backends
- **Response**: 
```json
{
  "backends": [
    {
      "name": "ollama",
      "type": "ollama",
      "is_available": true,
      "last_checked": 1766073015.724878,
      "config": {}
    },
    {
      "name": "openrouter",
      "type": "openrouter",
      "is_available": false,
      "last_checked": 1766073015.724881,
      "config": {}
    },
    {
      "name": "windowsml",
      "type": "windowsml",
      "is_available": false,
      "last_checked": 1766073015.72489,
      "config": {}
    },
    {
      "name": "contextual-fallback",
      "type": "contextualfallbackllm",
      "is_available": true,
      "last_checked": 1766073015.7248929,
      "config": {}
    }
  ]
}
```

### Backend Test
- **Status**: ✅ Success
- **Method**: POST
- **Endpoint**: /api/v1/management/backends/ollama/test
- **HTTP Status**: 200
- **Description**: Test backend connectivity
- **Response**: 
```json
{
  "success": true,
  "latency_ms": 0.00095367431640625,
  "error": null
}
```

### Context Config Get
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /api/v1/management/context/config
- **HTTP Status**: 200
- **Description**: Get context configuration
- **Response**: 
```json
{
  "extra_documents_dir": null,
  "enable_semantic_chunking": true,
  "max_combined_context_tokens": 8192
}
```

### Context Config Put
- **Status**: ✅ Success
- **Method**: PUT
- **Endpoint**: /api/v1/management/config/context
- **HTTP Status**: 200
- **Description**: Update context configuration
- **Response**: 
```json
{
  "extra_documents_dir": null,
  "enable_semantic_chunking": true,
  "max_combined_context_tokens": 8192
}
```

### Security Status
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /api/v1/management/security/status
- **HTTP Status**: 200
- **Description**: Get security status
- **Response**: 
```json
{
  "api_keys_count": 0,
  "audit_log_enabled": false
}
```

### Persona Create
- **Status**: ✅ Success
- **Method**: POST
- **Endpoint**: /api/v1/management/personas
- **HTTP Status**: 200
- **Description**: Create new persona
- **Response**: 
```json
{
  "name": "test-persona",
  "description": "Test persona for endpoint testing",
  "system_prompt": "You are a helpful test assistant.",
  "max_context_window": 2048,
  "routing_hint": "test",
  "is_active": true
}
```

### Persona Update
- **Status**: ✅ Success
- **Method**: PUT
- **Endpoint**: /api/v1/management/personas/test-persona
- **HTTP Status**: 200
- **Description**: Update persona
- **Response**: 
```json
{
  "name": "test-persona",
  "description": "Updated test persona description",
  "system_prompt": "You are a helpful test assistant with updated instructions.",
  "max_context_window": 2048,
  "routing_hint": "test",
  "is_active": true
}
```

### Openai Chat
- **Status**: ❌ Failed
- **Method**: POST
- **Endpoint**: /v1/chat/completions
- **HTTP Status**: 500
- **Description**: OpenAI-compatible chat completions
- **Response**: 
```json
"Internal Server Error"
```

### Openai Models
- **Status**: ✅ Success
- **Method**: GET
- **Endpoint**: /v1/models
- **HTTP Status**: 200
- **Description**: OpenAI-compatible models list
- **Response**: 
```json
{
  "object": "list",
  "data": [
    {
      "id": "llama3.2:latest",
      "object": "model",
      "created": 1766073015,
      "owned_by": "jarvis"
    }
  ]
}
```

### Config Save
- **Status**: ✅ Success
- **Method**: POST
- **Endpoint**: /api/v1/management/config/save
- **HTTP Status**: 200
- **Description**: Save configuration
- **Response**: 
```json
{
  "success": true,
  "config_hash": "62095714ce57270d",
  "message": "Configuration saved successfully (in-memory only for now)"
}
```

### Persona Delete
- **Status**: ✅ Success
- **Method**: DELETE
- **Endpoint**: /api/v1/management/personas/test-persona
- **HTTP Status**: 200
- **Description**: Delete test persona
- **Response**: 
```json
{
  "message": "Persona 'test-persona' deleted successfully"
}
```

## Response Schema Analysis

### Successful Response Schemas

#### 1. /health
```json
{
  "status": "ok",
  "available_models": [
    "ollama",
    "contextual-fallback"
  ]
}
```

#### 2. /api/v1/models
**Response**: ['ollama', 'contextual-fallback']

#### 3. /api/v1/personas
**Response**: [{'name': 'generalist', 'description': 'Balanced assistant persona', 'max_context_window': 4096, 'routing_hint': 'general'}]

#### 4. /api/v1/monitoring/metrics
```json
{
  "history": [
    {
      "request_count": 0,
      "average_latency_ms": 0.0,
      "max_latency_ms": 0.0,
      "tokens_generated": 0,
      "context_tokens": 0,
      "personas_used": {},
      "timestamp": 1766072994.55075
    }
  ]
}
```

#### 5. /api/v1/monitoring/traces
```json
{
  "traces": []
}
```

