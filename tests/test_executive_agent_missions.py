import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from jarvis.ecosystem.meta_intelligence import ExecutiveAgent
from jarvis.agents.mission_planner import MissionPlanner
from jarvis.orchestration.sub_orchestrator import SubOrchestrator
from jarvis.memory.project_memory import ProjectMemory
from jarvis.world_model.knowledge_graph import KnowledgeGraph
from jarvis.orchestration.mission import MissionDAG

# --- Mock Fixtures ---

@pytest.fixture
def mock_mcp_client():
    return MagicMock()

@pytest.fixture
def mock_mission_planner():
    planner = MagicMock(spec=MissionPlanner)

    # Create a mock MissionDAG object
    mock_dag = MagicMock(spec=MissionDAG)
    mock_dag.to_dict.return_value = {
        "nodes": {
            "step1": {"id": "step1", "details": "First step", "specialists": ["coder"]},
            "step2": {"id": "step2", "details": "Second step", "specialists": ["tester"]},
        },
        "edges": [("step1", "step2")]
    }

    # The 'tasks' attribute should be a list of dicts
    mock_dag.tasks = [
        {"id": "step1", "details": "First step", "specialists": ["coder"]},
        {"id": "step2", "details": "Second step", "specialists": ["tester"]},
    ]

    # The plan method should return the mock DAG
    planner.plan.return_value = mock_dag

    # The to_graph method should return a dict
    planner.to_graph.return_value = {"nodes": {}, "edges": []}

    return planner

@pytest.fixture
def mock_sub_orchestrator():
    orchestrator = AsyncMock(spec=SubOrchestrator)
    orchestrator.coordinate_specialists.return_value = {"success": True, "result": "step completed"}
    return orchestrator

@pytest.fixture
def executive_agent(mock_mcp_client, mock_mission_planner):
    """An ExecutiveAgent configured with mock dependencies."""
    agent = ExecutiveAgent(
        agent_id="test_agent",
        mcp_client=mock_mcp_client,
        mission_planner=mock_mission_planner,
        enable_curiosity=False, # Disabled by default for most tests
    )
    # Replace the orchestrator class with a mock to check constructor calls
    agent.orchestrator_cls = MagicMock(return_value=mock_sub_orchestrator)
    agent.curiosity_agent = MagicMock() # Mock the curiosity agent
    return agent

# --- Test Cases ---

@pytest.mark.asyncio
async def test_execute_mission_success(executive_agent):
    """Test a successful multi-step mission execution."""
    executive_agent.execute_task = AsyncMock(return_value={"success": True, "result": "step completed"})

    result = await executive_agent.execute_mission("test directive", {})

    assert result["success"]
    assert len(result["results"]) == 2

    # Check that the mission planner was called
    executive_agent.mission_planner.plan.assert_called_once_with("test directive", {})

    # Check that execute_task was called for each step
    assert executive_agent.execute_task.call_count == 2
    first_call_task = executive_agent.execute_task.call_args_list[0][0][0]
    assert first_call_task['type'] == 'mission_step'
    assert first_call_task['step_id'] == 'step1'

@pytest.mark.asyncio
async def test_execute_mission_failure(executive_agent):
    """Test that the mission aborts if a step fails."""
    # Make the second step fail
    results = [
        {"success": True, "result": "step completed"},
        {"success": False, "error": "step failed"},
    ]
    async def side_effect(*args, **kwargs):
        return results.pop(0)

    executive_agent.execute_task = AsyncMock(side_effect=side_effect)

    result = await executive_agent.execute_mission("test directive", {})

    assert not result["success"]
    assert "Mission failed at step step2" in result["error"]
    assert len(result["results"]) == 2

@pytest.mark.asyncio
async def test_pass_memory_and_kg_to_sub_orchestrator(executive_agent):
    """Test that memory and kg are passed to sub-orchestrators."""
    executive_agent.knowledge_graph = "my_kg"
    executive_agent.memory = "my_memory"

    # Mock the create_sub_orchestrator method
    executive_agent.create_sub_orchestrator = MagicMock(return_value=AsyncMock())

    await executive_agent.execute_mission("test directive", {})

    assert executive_agent.create_sub_orchestrator.call_count == 2

    # Check the spec of the first call
    first_call_args = executive_agent.create_sub_orchestrator.call_args_list[0]
    spec = first_call_args[0][1] # spec is the second positional argument
    assert spec['knowledge_graph'] == 'my_kg'
    assert spec['memory'] == 'my_memory'

    # Check the spec of the second call
    second_call_args = executive_agent.create_sub_orchestrator.call_args_list[1]
    spec = second_call_args[0][1]
    assert spec['knowledge_graph'] == 'my_kg'
    assert spec['memory'] == 'my_memory'

@pytest.mark.asyncio
async def test_curiosity_agent_trigger(executive_agent):
    """Test that curiosity is triggered when enabled."""
    executive_agent.enable_curiosity = True
    executive_agent.curiosity_agent.generate_question.return_value = "What is love?"
    executive_agent.log_event = MagicMock()

    # Mock execute_task to avoid running the full mission logic
    executive_agent.execute_task = AsyncMock(return_value={"success": True})

    await executive_agent.execute_mission("test directive", {})

    executive_agent.curiosity_agent.generate_question.assert_called_once()
    executive_agent.log_event.assert_called_once_with(
        "curiosity_triggered", {"question": "What is love?"}
    )
