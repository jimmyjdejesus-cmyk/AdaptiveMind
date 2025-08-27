import React, { useState, useEffect, useCallback } from 'react';
import { http } from '@tauri-apps/api';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  ConnectionLineType,
  Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { socket } from '../socket';

// Custom node types for different workflow stages
const nodeTypes = {
  start: ({ data }) => (
    <div className="workflow-node start-node">
      <div className="node-header">🚀 Start</div>
      <div className="node-content">{data.label}</div>
    </div>
  ),
  agent: ({ data }) => (
    <div className="workflow-node agent-node">
      <div className="node-header">🤖 {data.agent || 'Agent'}</div>
      <div className="node-content">{data.label}</div>
      {data.reasoning && (
        <div className="node-reasoning">{data.reasoning}</div>
      )}
    </div>
  ),
  task: ({ data }) => (
    <div className="workflow-node task-node">
      <div className="node-header">⚡ Task</div>
      <div className="node-content">{data.label}</div>
      {data.status && (
        <div className={`node-status status-${data.status}`}>
          {data.status.replace('_', ' ').toUpperCase()}
        </div>
      )}
    </div>
  ),
  decision: ({ data }) => (
    <div className="workflow-node decision-node">
      <div className="node-header">🤔 Decision</div>
      <div className="node-content">{data.label}</div>
    </div>
  ),
  end: ({ data }) => (
    <div className="workflow-node end-node">
      <div className="node-header">🎯 Complete</div>
      <div className="node-content">{data.label}</div>
    </div>
  ),
};

const WorkflowPane = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sessionId, setSessionId] = useState('default-session');
  const [workflowStats, setWorkflowStats] = useState({
    totalNodes: 0,
    completedNodes: 0,
    failedNodes: 0,
    pendingNodes: 0
  });

  // Transform backend workflow data to React Flow format
  const transformWorkflowData = useCallback((workflowData) => {
    if (!workflowData || !workflowData.nodes) {
      return { nodes: [], edges: [] };
    }

    const transformedNodes = workflowData.nodes.map(node => ({
      id: node.id,
      type: node.type || 'task',
      position: node.position || { x: 0, y: 0 },
      data: {
        ...node.data,
        status: node.status,
        reasoning: node.reasoning,
        tool_outputs: node.tool_outputs
      },
      className: `status-${node.status}`,
    }));

    const transformedEdges = workflowData.edges.map(edge => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      type: edge.type || 'default',
      animated: edge.animated || false,
      label: edge.label,
      style: {
        stroke: edge.animated ? '#10b981' : '#6b7280',
        strokeWidth: edge.animated ? 3 : 2,
      },
    }));

    return { nodes: transformedNodes, edges: transformedEdges };
  }, []);

  // Calculate workflow statistics
  const calculateStats = useCallback((nodes) => {
    const stats = {
      totalNodes: nodes.length,
      completedNodes: 0,
      failedNodes: 0,
      pendingNodes: 0,
      runningNodes: 0,
      deadEndNodes: 0,
      hitlNodes: 0
    };

    nodes.forEach(node => {
      const status = node.data?.status || 'pending';
      switch (status) {
        case 'completed':
          stats.completedNodes++;
          break;
        case 'failed':
          stats.failedNodes++;
          break;
        case 'running':
          stats.runningNodes++;
          break;
        case 'dead_end':
          stats.deadEndNodes++;
          break;
        case 'hitl_required':
          stats.hitlNodes++;
          break;
        default:
          stats.pendingNodes++;
      }
    });

    return stats;
  }, []);

  // Fetch workflow data from backend
  const fetchWorkflow = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await http.fetch(`http://127.0.0.1:8000/api/workflow/${sessionId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const workflowData = response.data;
      const { nodes: transformedNodes, edges: transformedEdges } = transformWorkflowData(workflowData);
      
      setNodes(transformedNodes);
      setEdges(transformedEdges);
      setWorkflowStats(calculateStats(transformedNodes));
      
    } catch (e) {
      console.error("Failed to fetch workflow:", e);
      setError(`Failed to load workflow data: ${e.message}`);
    } finally {
      setLoading(false);
    }
  }, [sessionId, transformWorkflowData, setNodes, setEdges, calculateStats]);

  // Initial data fetch
  useEffect(() => {
    fetchWorkflow();
  }, [fetchWorkflow]);

  // WebSocket listeners for real-time updates
  useEffect(() => {
    const handleWorkflowUpdate = (data) => {
      console.log('Workflow update received:', data);
      const { nodes: transformedNodes, edges: transformedEdges } = transformWorkflowData(data);
      setNodes(transformedNodes);
      setEdges(transformedEdges);
      setWorkflowStats(calculateStats(transformedNodes));
    };

    const handleTaskProgress = (data) => {
      console.log('Task progress received:', data);
      // Update specific node status
      setNodes(currentNodes => 
        currentNodes.map(node => 
          node.id === data.task_id 
            ? { ...node, data: { ...node.data, ...data }, className: `status-${data.status}` }
            : node
        )
      );
    };

    const handleHitlRequest = (data) => {
      console.log('HITL request received:', data);
      // Update node to show HITL required status
      setNodes(currentNodes => 
        currentNodes.map(node => 
          node.id === data.task_id 
            ? { ...node, data: { ...node.data, status: 'hitl_required' }, className: 'status-hitl_required' }
            : node
        )
      );
    };

    const handleDeadEndAdded = (data) => {
      console.log('Dead-end task added:', data);
      setNodes(currentNodes => 
        currentNodes.map(node => 
          node.id === data.task_id 
            ? { ...node, data: { ...node.data, status: 'dead_end' }, className: 'status-dead_end' }
            : node
        )
      );
    };

    // Register WebSocket event listeners
    socket.on('workflow_updated', handleWorkflowUpdate);
    socket.on('task_progress', handleTaskProgress);
    socket.on('hitl_request', handleHitlRequest);
    socket.on('dead_end_added', handleDeadEndAdded);

    // Cleanup listeners on unmount
    return () => {
      socket.off('workflow_updated', handleWorkflowUpdate);
      socket.off('task_progress', handleTaskProgress);
      socket.off('hitl_request', handleHitlRequest);
      socket.off('dead_end_added', handleDeadEndAdded);
    };
  }, [transformWorkflowData, setNodes, calculateStats]);

  // Handle new connections between nodes
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // Handle node click for detailed view
  const onNodeClick = useCallback((event, node) => {
    console.log('Node clicked:', node);
    // Could emit event to show node details in sidebar
    socket.emit('node_selected', { node_id: node.id, session_id: sessionId });
  }, [sessionId]);

  // Trigger workflow simulation for testing
  const triggerSimulation = useCallback(async () => {
    try {
      await http.fetch(`http://127.0.0.1:8000/api/workflow/${sessionId}/simulate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    } catch (e) {
      console.error('Failed to trigger simulation:', e);
    }
  }, [sessionId]);

  return (
    <div className="pane workflow-pane">
      <div className="pane-header">
        <h2>🌌 Workflow Galaxy</h2>
        <div className="workflow-controls">
          <button onClick={fetchWorkflow} className="btn-refresh" disabled={loading}>
            {loading ? '⟳' : '🔄'} Refresh
          </button>
          <button onClick={triggerSimulation} className="btn-simulate">
            ⚡ Simulate
          </button>
        </div>
      </div>

      {/* Workflow Statistics Panel */}
      <div className="workflow-stats">
        <div className="stat-item">
          <span className="stat-label">Total:</span>
          <span className="stat-value">{workflowStats.totalNodes}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">✅ Complete:</span>
          <span className="stat-value">{workflowStats.completedNodes}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">⚡ Running:</span>
          <span className="stat-value">{workflowStats.runningNodes}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">⏳ Pending:</span>
          <span className="stat-value">{workflowStats.pendingNodes}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">❌ Failed:</span>
          <span className="stat-value">{workflowStats.failedNodes}</span>
        </div>
        {workflowStats.hitlNodes > 0 && (
          <div className="stat-item">
            <span className="stat-label">🤝 HITL:</span>
            <span className="stat-value">{workflowStats.hitlNodes}</span>
          </div>
        )}
        {workflowStats.deadEndNodes > 0 && (
          <div className="stat-item">
            <span className="stat-label">💀 Dead-End:</span>
            <span className="stat-value">{workflowStats.deadEndNodes}</span>
          </div>
        )}
      </div>

      <div className="pane-content workflow-canvas">
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
            <button onClick={fetchWorkflow} className="btn-retry">
              Try Again
            </button>
          </div>
        )}
        
        {loading && !error && (
          <div className="loading-message">
            <span className="loading-spinner">⟳</span>
            <span>Loading workflow...</span>
          </div>
        )}

        {!loading && !error && (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
            nodeTypes={nodeTypes}
            connectionLineType={ConnectionLineType.SmoothStep}
            fitView
            attributionPosition="bottom-left"
          >
            <Controls />
            <MiniMap 
              nodeColor={(node) => {
                switch (node.data?.status) {
                  case 'completed': return '#10b981';
                  case 'running': return '#3b82f6';
                  case 'failed': return '#ef4444';
                  case 'dead_end': return '#6b7280';
                  case 'hitl_required': return '#f59e0b';
                  default: return '#8b5cf6';
                }
              }}
              maskColor="rgba(0, 0, 0, 0.1)"
            />
            <Background variant="dots" gap={20} size={1} />
            
            <Panel position="top-right">
              <div className="workflow-legend">
                <div className="legend-title">Status Legend</div>
                <div className="legend-item">
                  <div className="legend-color status-completed"></div>
                  <span>Completed</span>
                </div>
                <div className="legend-item">
                  <div className="legend-color status-running"></div>
                  <span>Running</span>
                </div>
                <div className="legend-item">
                  <div className="legend-color status-pending"></div>
                  <span>Pending</span>
                </div>
                <div className="legend-item">
                  <div className="legend-color status-failed"></div>
                  <span>Failed</span>
                </div>
                <div className="legend-item">
                  <div className="legend-color status-hitl_required"></div>
                  <span>HITL Required</span>
                </div>
                <div className="legend-item">
                  <div className="legend-color status-dead_end"></div>
                  <span>Dead End</span>
                </div>
              </div>
            </Panel>
          </ReactFlow>
        )}
      </div>
    </div>
  );
};

export default WorkflowPane;
