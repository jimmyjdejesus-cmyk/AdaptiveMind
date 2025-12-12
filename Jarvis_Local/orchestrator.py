# In orchestrator.py __init__
from logger_config import log
from agents.meta_agent.agent import MetaAgent
from agents.specialists.coding_specialist.agent import CodingAgent
from agents.specialists.research_specialist.agent import ResearchAgent
# Import other agents as needed

def __init__(self):
    log.info("Initializing Orchestrator and agents...")
    # No more model loading! It's handled by Ollama.

    # ---Initialize agents ---
    self.meta_agent = MetaAgent()
    self.coding_agent = CodingAgent()
    self.research_agent = ResearchAgent()
    # --- Initialize other agents as needed
    self.history = []
    log.info("Orchestrator initialization complete.")