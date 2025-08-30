"""
Base classes for all AI agents in the Jarvis system.
"""
from __future__ import annotations
from abc import abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from jarvis.agents.agent_resources import (
    AgentCapability,
    AgentMetrics,
)
from jarvis.world_model.knowledge_graph import KnowledgeGraph


class AIAgent:
    """Abstract base class for all AI agents."""

    def __init__(self, agent_id: str, capabilities: List[AgentCapability], knowledge_graph: Optional[KnowledgeGraph] = None):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.metrics = AgentMetrics(agent_id)
        self.created_at = datetime.now()
        self.is_active = True
        self.knowledge_graph = knowledge_graph

    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task and return results"""
        pass

    @abstractmethod
    async def learn_from_feedback(self, feedback: Dict[str, Any]) -> bool:
        """Learn from feedback and adapt behavior"""
        pass

    def update_metrics(self, success: bool, response_time: float, resource_usage: float):
        """Update agent performance metrics"""
        alpha = 0.1
        if success:
            self.metrics.success_rate = (1 - alpha) * self.metrics.success_rate + alpha * 1.0
        else:
            self.metrics.success_rate = (1 - alpha) * self.metrics.success_rate + alpha * 0.0
        self.metrics.average_response_time = (
            (1 - alpha) * self.metrics.average_response_time + alpha * response_time
        )
        self.metrics.resource_usage = (
            (1 - alpha) * self.metrics.resource_usage + alpha * resource_usage
        )
        self.metrics.last_updated = datetime.now()

    def set_knowledge_graph(self, graph: KnowledgeGraph) -> None:
        """Attach a :class:`KnowledgeGraph` instance to this agent."""
        self.knowledge_graph = graph

    def query_knowledge_graph(self, query: str) -> Any:
        """Query the attached knowledge graph."""
        if not self.knowledge_graph:
            raise ValueError("KnowledgeGraph not available")
        return self.knowledge_graph.query(query)
