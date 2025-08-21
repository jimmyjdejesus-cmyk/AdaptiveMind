"""
🚀 PHASE 5: META-INTELLIGENCE CORE (Refactored)

This module provides the MetaAgent, a high-level coordinator for the Jarvis AI ecosystem.
It uses a dynamic, LangGraph-based orchestrator to manage specialist agents.
"""
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

from langgraph.graph import END
from ..orchestration.orchestrator import DynamicOrchestrator, AgentSpec
from ..agents.specialists import CodeReviewAgent, SecurityAgent, ArchitectureAgent, TestingAgent, DevOpsAgent

logger = logging.getLogger(__name__)


class MetaAgent:
    """
    The MetaAgent manages and coordinates other AI agents to accomplish complex tasks.
    It uses a DynamicOrchestrator to create and run mission-specific workflows.
    """

    def __init__(self, agent_id: str, mcp_client=None):
        self.agent_id = agent_id
        self.mcp_client = mcp_client
        self.mission_orchestrators: Dict[str, DynamicOrchestrator] = {}
        
        # This would be dynamically loaded in a real system
        self.specialists = {
            "code_review": CodeReviewAgent(mcp_client),
            "security": SecurityAgent(mcp_client),
            "architecture": ArchitectureAgent(mcp_client),
            "testing": TestingAgent(mcp_client),
            "devops": DevOpsAgent(mcp_client),
        }

    async def coordinate_specialists(self, request: str, code: str = None) -> Dict[str, Any]:
        """
        Coordinates specialists to handle a request. This is the primary entry point.
        """
        # 1. Analyze the request to determine which specialists are needed.
        needed_specialists = self._analyze_request(request, code)

        if not needed_specialists:
            return {"synthesized_response": "No specialist analysis required for this request."}

        # 2. Create AgentSpec objects for the required specialists.
        agent_specs = self._create_agent_specs(needed_specialists)

        # 3. Create a DynamicOrchestrator for this mission.
        mission_id = str(uuid.uuid4())
        orchestrator = DynamicOrchestrator(agent_specs)
        self.mission_orchestrators[mission_id] = orchestrator

        # 4. Define the initial state for the workflow.
        initial_state = {
            "request": request,
            "code": code,
            "results": {},
        }

        # 5. Run the workflow.
        final_state = await orchestrator.run(initial_state)

        # 6. Synthesize the final response.
        synthesized_response = self._synthesize_results(final_state.get("results", {}))

        return {
            "type": "dynamic_orchestration",
            "specialists_used": needed_specialists,
            "results": final_state.get("results", {}),
            "synthesized_response": synthesized_response,
        }

    def _analyze_request(self, request: str, code: str = None) -> List[str]:
        """
        A simplified analysis to determine which specialists are needed.
        """
        request_lower = request.lower()
        needed = []
        if "review" in request_lower or code:
            needed.append("code_review")
        if "security" in request_lower:
            needed.append("security")
        if "architecture" in request_lower:
            needed.append("architecture")
        if "test" in request_lower:
            needed.append("testing")
        if "deploy" in request_lower:
            needed.append("devops")
        return needed

    def _create_agent_specs(self, specialist_names: List[str]) -> List[AgentSpec]:
        """
        Creates a list of AgentSpec objects for the given specialists.
        This defines a simple sequential workflow.
        """
        specs = []
        for i, name in enumerate(specialist_names):
            specialist = self.specialists.get(name)
            if not specialist:
                logger.warning(f"Specialist '{name}' not found.")
                continue

            # Define the function for the agent to execute
            async def agent_fn(state: Dict[str, Any], agent_name=name) -> Dict[str, Any]:
                agent = self.specialists[agent_name]
                request = state["request"]
                code = state.get("code")
                context = state.get("results", {})

                task = f"{request}\n\nCode:\n{code}" if code else request
                result = await agent.process_task(task, context=list(context.values()))

                state["results"][agent_name] = result
                return state

            # Create the AgentSpec
            spec = AgentSpec(
                name=name,
                fn=agent_fn,
                entry=(i == 0), # First specialist is the entry point
                next=specialist_names[i + 1] if i < len(specialist_names) - 1 else END,
            )
            specs.append(spec)

        return specs

    def _synthesize_results(self, results: Dict[str, Any]) -> str:
        """
        A simplified synthesis of the results from the specialists.
        """
        if not results:
            return "No results to synthesize."

        response = "## Multi-Agent Analysis\n\n"
        for specialist, result in results.items():
            response += f"### {specialist.title()} Insights\n"
            response += result.get("response", "No response provided.") + "\n\n"

        return response

__all__ = ["MetaAgent"]
