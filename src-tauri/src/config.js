const API_CONFIG = {
  // Backend base URLs
  HTTP_BASE_URL: storedHttp,
  WS_BASE_URL: storedWs,
  
  // API endpoints
  ENDPOINTS: {
    WORKFLOW: (sessionId) => `/api/workflow/${sessionId}`,
    WORKFLOW_SIMULATE: (sessionId) => `/api/workflow/${sessionId}/simulate`,
    LOGS: '/api/logs',
    LOGS_LATEST: '/logs/latest',
    HITL_PENDING: '/api/hitl/pending',
    HITL_APPROVE: (requestId) => `/api/hitl/${requestId}/approve`,
    HITL_DENY: (requestId) => `/api/hitl/${requestId}/deny`,
    DEAD_ENDS: (sessionId) => `/api/dead-ends?session_id=${sessionId}`,
    DEAD_END_RETRY: (taskId) => `/api/dead-ends/${taskId}/retry`,
    HEALTH: '/health',
    NEO4J_CONFIG: '/api/neo4j/config'
  }
};