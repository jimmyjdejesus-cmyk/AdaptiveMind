"""
The Unified Jarvis Agent

This module contains the primary, unified JarvisAgent class, which consolidates
the features of the simple, MCP, enhanced, and workflow agents into a single,
configurable class.
"""
import asyncio
import logging
from typing import Optional, Dict, Any, List

from ..mcp import MCPClient, ModelRouter, MCPServerManager
from ..ecosystem.meta_intelligence import MetaAgent
from ..workflows.engine import WorkflowEngine

logger = logging.getLogger(__name__)

class JarvisAgent:
    """
    The unified Jarvis agent, combining all capabilities into a single class.
    """

    def __init__(
        self,
        enable_mcp: bool = True,
        enable_multi_agent: bool = True,
        enable_workflows: bool = True,
    ):
        """
        Initializes the unified Jarvis agent.

        Args:
            enable_mcp: Enables multi-model capabilities via MCP.
            enable_multi_agent: Enables multi-agent orchestration.
            enable_workflows: Enables automated workflow execution.
        """
        self.enable_mcp = enable_mcp
        self.enable_multi_agent = enable_multi_agent
        self.enable_workflows = enable_workflows

        self.conversation_history = []

        # Initialize components based on configuration
        self.mcp_client = MCPClient() if enable_mcp else None
        self.server_manager = MCPServerManager(self.mcp_client) if enable_mcp else None
        self.model_router = ModelRouter(self.mcp_client) if enable_mcp else None
        self.orchestrator = MetaAgent("meta", mcp_client=self.mcp_client) if enable_multi_agent else None
        self.workflow_engine = WorkflowEngine() if enable_workflows else None

        self.mcp_initialized = False
        self.multi_agent_initialized = False

    async def chat_async(self, message: str, **kwargs) -> str:
        """
        Asynchronous chat entry point for the unified agent.
        """
        # 1. Add message to history
        self.conversation_history.append(
            {"role": "user", "content": message, "timestamp": asyncio.get_event_loop().time()}
        )

        # 2. Decide on the execution path
        if self.enable_workflows and await self._is_workflow_required(message):
            response = await self._execute_workflow(message, **kwargs)
        elif self.enable_multi_agent and await self._is_multi_agent_required(message, **kwargs):
            response = await self._execute_multi_agent(message, **kwargs)
        elif self.enable_mcp:
            response = await self._execute_mcp(message)
        else:
            response = self._simple_chat(message)

        # 3. Add response to history
        self.conversation_history.append(
            {"role": "assistant", "content": response, "timestamp": asyncio.get_event_loop().time()}
        )
        return response

    def chat(self, message: str, **kwargs) -> str:
        """
        Synchronous wrapper for the chat functionality.
        """
        try:
            return asyncio.run(self.chat_async(message, **kwargs))
        except Exception as e:
            logger.error(f"Error in synchronous chat: {e}")
            return self._simple_chat(message)

    def _simple_chat(self, message: str) -> str:
        """
        A basic chat implementation that uses the MCP client directly.
        """
        if self.mcp_client:
            try:
                # This is a simplified implementation. A real implementation would
                # have a more robust way of handling this.
                return asyncio.run(self.mcp_client.generate_response("ollama", "llama3.2", message))
            except Exception as e:
                logger.error(f"Simple chat with MCP client failed: {e}")
                return "I'm sorry, I'm having trouble connecting to the AI service."
        return "I'm sorry, I'm running in a limited mode and cannot process your request."


    async def _is_workflow_required(self, message: str) -> bool:
        keywords = ["workflow", "automate", "process", "pipeline"]
        return any(keyword in message.lower() for keyword in keywords)

    async def _is_multi_agent_required(self, message: str, **kwargs) -> bool:
        if kwargs.get("code"):
            return True
        keywords = ["review", "analyze", "refactor", "design", "security", "test", "deploy"]
        return any(keyword in message.lower() for keyword in keywords)

    async def _execute_workflow(self, message: str, **kwargs) -> str:
        # This will be implemented in a future step
        return "Workflow execution is not yet fully implemented."

    async def _execute_multi_agent(self, message: str, **kwargs) -> str:
        if not self.orchestrator:
            return await self._execute_mcp(message)
        
        try:
            code = kwargs.get("code")
            result = await self.orchestrator.coordinate_specialists(message, code)
            return self._format_multi_agent_response(result)
        except Exception as e:
            logger.error(f"Multi-agent execution failed: {e}")
            return await self._execute_mcp(message)

    async def _execute_mcp(self, message: str) -> str:
        if not self.model_router:
            return self._simple_chat(message)
        
        try:
            return await self.model_router.route_to_best_model(message)
        except Exception as e:
            logger.error(f"MCP execution failed: {e}")
            return self._simple_chat(message)

    def _format_multi_agent_response(self, result: Dict[str, Any]) -> str:
        """
        Formats the response from the multi-agent orchestrator into a rich,
        user-friendly output.
        """
        if not result or "synthesized_response" not in result:
            return "Multi-agent analysis failed to produce a response."

        response_parts = [
            "🧠 **Multi-Agent Analysis Complete**\n",
            f"**Specialists Consulted:** {', '.join(result.get('specialists_used', ['N/A']))}",
            "---",
            "**Synthesized Response:**",
            result['synthesized_response'],
        ]

        individual_results = result.get("results", {})
        if individual_results:
            response_parts.append("\n---\n**Individual Specialist Insights:**\n")
            for specialist, res in individual_results.items():
                response_parts.append(f"**{specialist.title()} Expert:**")
                response_parts.append(res.get("response", "No detailed response provided."))
                response_parts.append("")

        return "\n".join(response_parts)

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Returns a dictionary of the agent's capabilities.
        """
        return {
            "mcp_enabled": self.enable_mcp,
            "multi_agent_enabled": self.enable_multi_agent,
            "workflows_enabled": self.enable_workflows,
            "available_specialists": list(self.orchestrator.specialists.keys()) if self.orchestrator else [],
        }
