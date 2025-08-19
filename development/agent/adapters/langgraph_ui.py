"""
Visualization components for LangGraph workflows
"""

class WorkflowVisualizer:
    """Visualization for LangGraph workflows."""
    
    def __init__(self):
        """Initialize the visualizer."""
        self.executions = []
        
    def add_execution(self, execution_data):
        """Add an execution result to the visualizer."""
        self.executions.append(execution_data)
        
    def render(self):
        """Render the workflow visualization."""
        return {"visualizations": self.executions}
    
def render_langgraph_ui(workflow, execution_data=None):
    """Render a LangGraph UI component."""
    visualizer = WorkflowVisualizer()
    if execution_data:
        visualizer.add_execution(execution_data)
    return visualizer.render()
