"""
Defines the hierarchical agent structure for the Jarvis V2 Orchestration System.
"""

import uuid
import os
from typing import List, Dict, Any, Callable
from jarvis.memory.memory_bus import MemoryBus
# from jarvis.orchestration.graph import MultiTeamOrchestrator # Moved to fix circular import
from jarvis.tools.web_tools import search_web

class TeamMemberAgent:
    """Base class for all team member agents."""
    def __init__(self, orchestrator: 'OrchestratorAgent', team_name: str):
        self.agent_id = f"{team_name.lower()}_{uuid.uuid4().hex[:8]}"
        self.orchestrator = orchestrator
        self.team = team_name
        self.tools: Dict[str, Callable] = {}

    def log(self, message: str, data: Dict[str, Any] = None):
        """Logs a message to the orchestrator's memory bus."""
        self.orchestrator.memory_bus.log_interaction(self.agent_id, self.team, message, data)

    def run(self, objective: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """The main execution logic for the agent. To be implemented by subclasses."""
        raise NotImplementedError("Each team member must implement the 'run' method.")

# Define the specialized teams
class RedAdversaryAgent(TeamMemberAgent):
    def __init__(self, orchestrator: 'OrchestratorAgent'):
        super().__init__(orchestrator, "Red")

class BlueAdversaryAgent(TeamMemberAgent):
    def __init__(self, orchestrator: 'OrchestratorAgent'):
        super().__init__(orchestrator, "Blue")

class YellowCompetitiveAgent(TeamMemberAgent):
    def __init__(self, orchestrator: 'OrchestratorAgent'):
        super().__init__(orchestrator, "Yellow")
        self.tools["web_search"] = search_web

    def run(self, objective: str, context: Dict[str, Any]) -> Dict[str, Any]:
        self.log("Starting web research to generate competitive ideas.")
        search_results = self.tools["web_search"](f"innovative ideas for {objective}")
        self.log("Web search complete.", data={"results": search_results})
        return {"research_summary": search_results}

class GreenCompetitiveAgent(TeamMemberAgent):
    def __init__(self, orchestrator: 'OrchestratorAgent'):
        super().__init__(orchestrator, "Green")

class WhiteSecurityAgent(TeamMemberAgent):
    def __init__(self, orchestrator: 'OrchestratorAgent'):
        super().__init__(orchestrator, "White")

class BlackInnovatorAgent(TeamMemberAgent):
    def __init__(self, orchestrator: 'OrchestratorAgent'):
        super().__init__(orchestrator, "Black")


class OrchestratorAgent:
    """
    Manages a set of five specialized teams to accomplish a complex objective.
    """
    def __init__(self, meta_agent: 'MetaAgent', objective: str, directory: str = ".", shared_bus: MemoryBus = None):
        self.agent_id = f"orchestrator_{uuid.uuid4().hex[:8]}"
        self.meta_agent = meta_agent
        self.objective = objective
        self.memory_bus = MemoryBus(directory) # Local bus for this project
        self.shared_bus = shared_bus # Shared bus for inter-orchestrator communication
        
        # Initialize the five teams
        self.teams = {
            "adversary_pair": (RedAdversaryAgent(self), BlueAdversaryAgent(self)),
            "competitive_pair": (YellowCompetitiveAgent(self), GreenCompetitiveAgent(self)),
            "security_quality": WhiteSecurityAgent(self),
            "innovators_disruptors": BlackInnovatorAgent(self),
        }
        
        # Initialize the LangGraph orchestrator
        from jarvis.orchestration.graph import MultiTeamOrchestrator # Local import to break cycle
        self.orchestrator = MultiTeamOrchestrator(self)
        
        self.log(f"Orchestrator initialized for objective: {objective}")

    def log(self, message: str, data: Dict[str, Any] = None):
        """Logs a message from the orchestrator itself to its local bus."""
        self.memory_bus.log_interaction(self.agent_id, "Orchestrator", message, data)

    def broadcast(self, message: str, data: Dict[str, Any] = None):
        """Broadcasts a significant finding to the shared memory bus for other orchestrators."""
        if self.shared_bus:
            self.shared_bus.log_interaction(self.agent_id, f"Broadcast | {self.objective[:30]}...", message, data)

    def run(self):
        """Executes the multi-team workflow to achieve the objective."""
        self.log("Starting multi-team orchestration...")
        result = self.orchestrator.run(self.objective)
        self.log("Multi-team orchestration finished.", data={"final_result": result})
        return result


class MetaAgent:
    """
    The top-level agent that oversees the entire operation and can spawn orchestrators.
    """
    def __init__(self, directory: str = "."):
        self.agent_id = f"meta_agent_{uuid.uuid4().hex[:8]}"
        self.orchestrators: List[OrchestratorAgent] = []
        # The MetaAgent manages the shared bus for all its orchestrators
        self.shared_memory_bus = MemoryBus(os.path.join(directory, "shared_orchestrator_bus"))
        self.log("Meta-Agent initialized and shared memory bus is active.")

    def log(self, message: str, data: Dict[str, Any] = None):
        """Logs a message from the Meta-Agent to the shared bus."""
        self.shared_memory_bus.log_interaction(self.agent_id, "Meta", message, data)

    def spawn_orchestrator(self, objective: str, directory: str = ".") -> OrchestratorAgent:
        """Dynamically creates and deploys an OrchestratorAgent for a new objective."""
        self.log(f"Spawning new orchestrator for objective: '{objective}' in directory '{directory}'.")
        orchestrator = OrchestratorAgent(self, objective, directory, shared_bus=self.shared_memory_bus)
        self.orchestrators.append(orchestrator)
        return orchestrator

# Example usage:
if __name__ == "__main__":
    # 1. The Meta-Agent is initialized
    meta_agent = MetaAgent()

    # 2. The user provides a high-level objective, and the Meta-Agent spawns an orchestrator
    objective = "Develop a secure and innovative user authentication module."
    project_directory = "auth_module_project"
    os.makedirs(project_directory, exist_ok=True)
    
    orchestrator = meta_agent.spawn_orchestrator(objective, project_directory)
    
    # 3. The orchestrator would then run its complex, multi-team workflow
    # orchestrator.run() # This will be implemented with LangGraph

    print(f"Meta-Agent spawned Orchestrator {orchestrator.agent_id} for objective: '{objective}'")
    print(f"Project logs will be in: {os.path.abspath(project_directory)}/agent.md")
