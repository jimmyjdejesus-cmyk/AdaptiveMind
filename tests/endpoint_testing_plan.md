# Endpoint Testing Plan

## Objective
Test all available endpoints and return data and schemas for the Jarvis_AI/AdaptiveMind project.

## Available Servers
- [ ] jarvis_core/server.py
- [ ] jarvis_core/minimal_server.py
- [ ] adaptivemind_core/server.py
- [ ] adaptivemind_core/minimal_server.py
- [ ] adaptivemind_core/server_enhanced.py
- [ ] adaptivemind_core/server_fixed.py
- [ ] adaptivemind_core/server_simple.py

## Testing Tasks
- [ ] 1. Analyze API schemas to identify all endpoints
- [ ] 2. Start available servers
- [ ] 3. Test core chat endpoints (/chat, /chat/completions)
- [ ] 4. Test LLM integration endpoints (Ollama)
- [ ] 5. Test agent management endpoints
- [ ] 6. Test memory/workflow endpoints
- [ ] 7. Test orchestration endpoints
- [ ] 8. Test monitoring endpoints
- [ ] 9. Test security endpoints
- [ ] 10. Test websocket endpoints
- [ ] 11. Document all responses and schemas
- [ ] 12. Generate comprehensive test report

## Tools to Use
- curl for HTTP requests
- Postman collection for organized testing
- jq for JSON response formatting
- pytest for automated testing
