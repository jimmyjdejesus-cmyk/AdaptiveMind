# Jarvis AI API v1 Reference

Base path: `/api/v1`
Auth: `X-API-Key: <JARVIS_API_KEY>` (set `JARVIS_DISABLE_AUTH=true` to bypass locally)

## Health
GET `/health`
- 200: `{ "status": "ok", "ollama": "ok|unavailable|error" }`

## Models
GET `/models`
- 200: `{ "models": ["llama3.1:8b-instruct-q4_K_M", ...] }`

## Chat
POST `/chat`
- Body: `{ messages: [{role, content}], model?, temperature?, max_tokens? }`
- 200: `{ content: string, model?: string }`

POST `/chat/stream`
- Same body as `/chat`
- 200: `text/plain` streaming chunks

## Agents
GET `/agents`
- 200: `{ agents: string[], count: number }`

POST `/agents/execute`
- Body: `{ agent_type, objective, context?, priority?, timeout? }`
- 200: execution result

POST `/agents/collaborate`
- Body: `{ agent_types: string[], objective, context? }`
- 200: collaboration result

GET `/agents/capabilities/{agent_type}`
- 200: capabilities for agent type

GET `/agents/bridge/list`
- 200: agents with status and capabilities

## Memory
GET `/memory/stats`
- 200: stats object

POST `/memory/sync/to-legacy` (DEPRECATED)
- 200: sync result

POST `/memory/sync/from-legacy` (DEPRECATED)
- 200: load result

POST `/memory/migrate`
- 200: migration result

## Workflows
POST `/workflows/execute`
- Body: `{ workflow_type, parameters?, priority?, timeout? }`
- 200: workflow result

GET `/workflows/capabilities`
- 200: workflows and capabilities

GET `/workflows/active`
- 200: active workflows

## Security
POST `/security/validate`
- Body: `{ agent_id, action, context? }`
- 200: validation result

GET `/security/events?limit=100`
- 200: events list

GET `/security/stats`
- 200: stats object

POST `/security/audit`
- 200: audit result

## Monitoring
GET `/monitoring/metrics`
- 200: metrics list

GET `/monitoring/summary?time_window_minutes=60`
- 200: summary object

GET `/monitoring/health`
- 200: health object

GET `/monitoring/performance`
- 200: performance object

GET `/monitoring/export?format=json`
- 200: export data

## Feed Ingestion
POST `/feed/ingest`
- Body: `{ items: [{id?, source?, content, metadata?}], persist_to_knowledge?: bool, persist_to_memory?: bool }`
- 200: `{ ingested, errors }`

## Jobs (Async)
POST `/jobs`
- Body: `{ mode: "chat"|"agent"|"workflow", payload: {}, callback_url?: string }`
- 200: `{ job_id, status: "queued" }`

GET `/jobs/{job_id}`
- 200: `{ job_id, status, result? }`
