"""
Dynamic Orchestrator using LangGraph

This module provides a light-weight, dynamic orchestration engine that builds
LangGraph workflows from simple agent specifications.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Optional

from langgraph.graph import END, StateGraph

logger = logging.getLogger(__name__)

# --- Agent Specification Model ---

AgentCallable = Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]

@dataclass
class AgentSpec:
    """
    Specification for a single node in the workflow graph.

    Attributes:
        name: The unique identifier for the node in the graph.
        fn: The callable (function or method) to be executed when the node runs.
        next: The name of the next node for a simple, linear transition.
        condition: A callable that determines the next branch to take.
        branches: A mapping from condition outputs to the name of the next node.
        entry: A boolean indicating if this node is the entry point of the graph.
    """
    name: str
    fn: AgentCallable
    next: Optional[str] = None
    condition: Optional[Callable[[Dict[str, Any]], str]] = None
    branches: Optional[Dict[str, str]] = None
    entry: bool = False


# --- Dynamic Orchestrator ---

class DynamicOrchestrator:
    """
    Builds and executes LangGraph workflows from a list of AgentSpec objects.
    """

    def __init__(self, agent_specs: List[AgentSpec]):
        """
        Initializes the DynamicOrchestrator.

        Args:
            agent_specs: A list of AgentSpec objects defining the workflow graph.
        """
        if not agent_specs:
            raise ValueError("At least one AgentSpec is required to build a workflow.")

        self.agent_specs = agent_specs
        self.workflow = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        Builds the StateGraph from the provided agent specifications.
        """
        graph = StateGraph(dict)

        # Add nodes to the graph
        for spec in self.agent_specs:
            graph.add_node(spec.name, spec.fn)

        # Set the entry point
        try:
            entry_point = next(s.name for s in self.agent_specs if s.entry)
        except StopIteration:
            entry_point = self.agent_specs[0].name
            logger.warning(f"No entry point specified. Defaulting to '{entry_point}'.")
        graph.set_entry_point(entry_point)

        # Add edges to the graph
        for spec in self.agent_specs:
            if spec.next:
                graph.add_edge(spec.name, spec.next)
            if spec.condition and spec.branches:
                graph.add_conditional_edges(spec.name, spec.condition, spec.branches)

        return graph.compile()

    async def run(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the compiled LangGraph workflow.

        Args:
            initial_state: The initial state to pass to the workflow.

        Returns:
            The final state of the workflow after execution.
        """
        logger.debug(f"Starting workflow with initial state: {initial_state}")
        final_state = await self.workflow.ainvoke(initial_state)
        logger.debug(f"Workflow completed with final state: {final_state}")
        return final_state

__all__ = ["AgentSpec", "DynamicOrchestrator", "END"]
