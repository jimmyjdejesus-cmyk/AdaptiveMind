"""Bridge between new agent system and legacy orchestration."""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LegacyAgentTask:
    """Legacy task format for agent execution."""
    task_id: str
    agent_type: str
    objective: str
    context: Dict[str, Any]
    priority: int = 1
    timeout: int = 300

class AgentBridge:
    """Bridge between new AgentManager and legacy orchestration."""
    
    def __init__(self, new_agent_manager=None, new_ollama_client=None):
        """Initialize the bridge.
        
        Args:
            new_agent_manager: New AgentManager instance
            new_ollama_client: New OllamaClient instance
        """
        self.new_agent_manager = new_agent_manager
        self.new_ollama_client = new_ollama_client
        self.agent_type_mapping = {
            "research": "research_agent",
            "coding": "coding_agent", 
            "curiosity": "curiosity_agent",
            "benchmark": "benchmark_agent",
            "default": "default_agent"
        }
    
    async def execute_legacy_task(self, task: LegacyAgentTask) -> Dict[str, Any]:
        """Execute a legacy task using new agent system.
        
        Args:
            task: Legacy task to execute
            
        Returns:
            Task result dictionary
        """
        if not self.new_agent_manager:
            return {"error": "New agent manager not available"}
        
        try:
            # Map legacy agent type to new agent
            agent_id = self.agent_type_mapping.get(task.agent_type, "default_agent")
            
            # Check if agent exists, create if needed
            if agent_id not in self.new_agent_manager.agents:
                await self._ensure_agent_exists(agent_id, task.agent_type)
            
            # Execute task using new agent manager
            result = await self.new_agent_manager.execute_task(
                agent_id=agent_id,
                task_type="legacy_execution",
                prompt=task.objective,
                context=task.context,
                timeout=task.timeout
            )
            
            return {
                "task_id": task.task_id,
                "agent_id": agent_id,
                "result": result.result if hasattr(result, 'result') else str(result),
                "success": not result.is_failed if hasattr(result, 'is_failed') else True,
                "duration": result.duration if hasattr(result, 'duration') else None,
                "error": result.error if hasattr(result, 'error') else None
            }
            
        except Exception as e:
            logger.error(f"Failed to execute legacy task {task.task_id}: {e}")
            return {
                "task_id": task.task_id,
                "error": str(e),
                "success": False
            }
    
    async def _ensure_agent_exists(self, agent_id: str, agent_type: str):
        """Ensure the specified agent exists in the new system."""
        try:
            # Import new agent types
            from jarvis.agents.research_agent import ResearchAgent
            from jarvis.agents.coding_agent import CodingAgent
            from jarvis.agents.curiosity_agent import CuriosityAgent
            from jarvis.agents.benchmark_agent import BenchmarkAgent
            from jarvis.agents.base import BaseAgent
            
            # Create appropriate agent based on type
            agent_classes = {
                "research_agent": ResearchAgent,
                "coding_agent": CodingAgent,
                "curiosity_agent": CuriosityAgent,
                "benchmark_agent": BenchmarkAgent,
                "default_agent": BaseAgent
            }
            
            agent_class = agent_classes.get(agent_id, BaseAgent)
            agent = agent_class(agent_id=agent_id)
            
            # Register with new agent manager
            self.new_agent_manager.register_agent(agent)
            
            logger.info(f"Created and registered agent {agent_id}")
            
        except Exception as e:
            logger.error(f"Failed to create agent {agent_id}: {e}")
            raise
    
    async def get_agent_capabilities(self, agent_type: str) -> Dict[str, Any]:
        """Get capabilities of a specific agent type."""
        agent_id = self.agent_type_mapping.get(agent_type, "default_agent")
        
        if not self.new_agent_manager or agent_id not in self.new_agent_manager.agents:
            return {"error": "Agent not available"}
        
        agent = self.new_agent_manager.get_agent(agent_id)
        if not agent:
            return {"error": "Agent not found"}
        
        return {
            "agent_id": agent_id,
            "agent_type": agent_type,
            "capabilities": getattr(agent, 'capabilities', []),
            "status": self.new_agent_manager.get_agent_status(agent_id).value if self.new_agent_manager.get_agent_status(agent_id) else "unknown"
        }
    
    async def list_available_agents(self) -> List[Dict[str, Any]]:
        """List all available agents with their capabilities."""
        if not self.new_agent_manager:
            return []
        
        agents = []
        for agent_id, agent in self.new_agent_manager.agents.items():
            # Find legacy agent type
            legacy_type = None
            for lt, nt in self.agent_type_mapping.items():
                if nt == agent_id:
                    legacy_type = lt
                    break
            
            agents.append({
                "agent_id": agent_id,
                "legacy_type": legacy_type or "unknown",
                "status": self.new_agent_manager.get_agent_status(agent_id).value if self.new_agent_manager.get_agent_status(agent_id) else "unknown",
                "capabilities": getattr(agent, 'capabilities', [])
            })
        
        return agents
    
    async def execute_collaboration(self, 
                                  agent_types: List[str], 
                                  objective: str, 
                                  context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a collaboration between multiple agents."""
        if not self.new_agent_manager:
            return {"error": "New agent manager not available"}
        
        try:
            # Ensure all agents exist
            for agent_type in agent_types:
                agent_id = self.agent_type_mapping.get(agent_type, "default_agent")
                if agent_id not in self.new_agent_manager.agents:
                    await self._ensure_agent_exists(agent_id, agent_type)
            
            # Create collaboration request
            from jarvis.core.agent_manager import CollaborationRequest, CollaborationMode
            
            request = CollaborationRequest(
                request_id=f"legacy_collab_{asyncio.get_event_loop().time()}",
                initiator_id="legacy_system",
                target_agents=[self.agent_type_mapping.get(at, "default_agent") for at in agent_types],
                task_description=objective,
                mode=CollaborationMode.PARALLEL,
                context=context or {}
            )
            
            # Execute collaboration
            result_id = await self.new_agent_manager.initiate_collaboration(request)
            
            # Wait for completion (simplified - in real implementation would poll)
            await asyncio.sleep(1)
            
            return {
                "collaboration_id": result_id,
                "agent_types": agent_types,
                "objective": objective,
                "status": "completed"  # Simplified
            }
            
        except Exception as e:
            logger.error(f"Failed to execute collaboration: {e}")
            return {"error": str(e), "success": False}

# Global bridge instance
agent_bridge = None

def initialize_agent_bridge(new_agent_manager=None, new_ollama_client=None):
    """Initialize the global agent bridge."""
    global agent_bridge
    agent_bridge = AgentBridge(new_agent_manager, new_ollama_client)
    return agent_bridge

def get_agent_bridge() -> Optional[AgentBridge]:
    """Get the global agent bridge instance."""
    return agent_bridge
