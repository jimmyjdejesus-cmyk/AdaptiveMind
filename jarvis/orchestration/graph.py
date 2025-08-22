"""
Defines the LangGraph-based orchestration logic for the multi-agent teams.
"""

from typing import List, Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
# from langgraph.checkpoints import SqliteSaver # Temporarily removed to resolve import error
from jarvis.orchestration.agents import OrchestratorAgent, TeamMemberAgent

# Define the state for our graph
class TeamWorkflowState(TypedDict):
    objective: str
    context: Dict[str, Any]
    team_outputs: Dict[str, Any]
    next_team: str

class MultiTeamOrchestrator:
    """
    Uses LangGraph to orchestrate the five specialized teams.
    """
    def __init__(self, orchestrator_agent: OrchestratorAgent):
        self.orchestrator = orchestrator_agent
        self.graph = self._build_graph()

    def _build_graph(self):
        """Constructs the LangGraph for the multi-team workflow."""
        graph = StateGraph(TeamWorkflowState)

        # Define nodes for each team's execution
        graph.add_node("adversary_pair", self._run_adversary_pair)
        graph.add_node("competitive_pair", self._run_competitive_pair)
        graph.add_node("security_quality", self._run_security_quality)
        graph.add_node("innovators_disruptors", self._run_innovators_disruptors)
        graph.add_node("broadcast_findings", self._broadcast_findings)

        # The graph starts with the competitive pair to generate initial ideas
        graph.set_entry_point("competitive_pair")

        # Define the workflow logic
        graph.add_edge("competitive_pair", "adversary_pair")
        graph.add_edge("adversary_pair", "innovators_disruptors")
        graph.add_edge("innovators_disruptors", "broadcast_findings") # Broadcast after innovation
        graph.add_edge("broadcast_findings", "security_quality")
        graph.add_edge("security_quality", END) # The White team is the final check

        # Temporarily compiling without a checkpointer to resolve import issues.
        # State will not be persisted between runs.
        return graph.compile()

    def _run_team(self, team: TeamMemberAgent, state: TeamWorkflowState) -> Dict[str, Any]:
        """Helper function to run a single team member."""
        # This now calls the agent's actual run method.
        # If the method is not implemented, it will use a default simulation.
        try:
            result = team.run(state['objective'], state['context'])
        except NotImplementedError:
            team.log(f"Starting simulated task for objective: {state['objective']}")
            result = {f"{team.team.lower()}_output": f"Completed simulated task for {team.team} team."}
            team.log(f"Simulated task finished.", data=result)
        return result

    def _run_adversary_pair(self, state: TeamWorkflowState) -> TeamWorkflowState:
        """Runs the Red and Blue teams in parallel."""
        red_agent, blue_agent = self.orchestrator.teams["adversary_pair"]
        
        # In a real implementation, this would use parallel execution (e.g., threading)
        red_output = self._run_team(red_agent, state)
        blue_output = self._run_team(blue_agent, state)

        state["team_outputs"]["adversary_pair"] = [red_output, blue_output]
        return state

    def _run_competitive_pair(self, state: TeamWorkflowState) -> TeamWorkflowState:
        """Runs the Yellow and Green teams in parallel."""
        yellow_agent, green_agent = self.orchestrator.teams["competitive_pair"]
        
        yellow_output = self._run_team(yellow_agent, state)
        green_output = self._run_team(green_agent, state)

        state["team_outputs"]["competitive_pair"] = [yellow_output, green_output]
        return state

    def _run_security_quality(self, state: TeamWorkflowState) -> TeamWorkflowState:
        """Runs the White team."""
        white_agent = self.orchestrator.teams["security_quality"]
        white_output = self._run_team(white_agent, state)
        state["team_outputs"]["security_quality"] = white_output
        return state

    def _run_innovators_disruptors(self, state: TeamWorkflowState) -> TeamWorkflowState:
        """Runs the Black team."""
        # This is where the special visibility rule applies.
        # The Black team's context would be filtered to exclude White team's outputs.
        black_agent = self.orchestrator.teams["innovators_disruptors"]
        
        # Create a filtered context for the Black team
        filtered_context = state["context"].copy()
        # In a real scenario, we would filter the memory bus view here.
        
        black_output = self._run_team(black_agent, state)
        state["team_outputs"]["innovators_disruptors"] = black_output
        return state

    def _broadcast_findings(self, state: TeamWorkflowState) -> TeamWorkflowState:
        """Broadcasts key findings from the innovator team to the shared bus."""
        innovator_output = state["team_outputs"].get("innovators_disruptors", {})
        if innovator_output:
            self.orchestrator.broadcast(
                "Broadcasting innovative findings for collective learning.",
                data=innovator_output
            )
        return state

    def run(self, objective: str):
        """Executes the full orchestration graph."""
        initial_state = {
            "objective": objective,
            "context": {},
            "team_outputs": {},
            "next_team": "competitive_pair"
        }
        
        # The `stream` method will execute the graph step-by-step
        for step in self.graph.stream(initial_state):
            # Each step is a dictionary with the node name and its output
            node, output = next(iter(step.items()))
            self.orchestrator.log(f"Completed step: {node}", data=output)
        
        return "Orchestration complete."
