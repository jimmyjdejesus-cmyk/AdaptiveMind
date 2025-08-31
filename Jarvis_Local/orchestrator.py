from agents.meta_agent.agent import MetaAgent
from agents.specialists.coding_specialist.agent import CodingAgent
from logger_config import log

class Orchestrator:
    def __init__(self):
        log.info("Initializing Orchestrator and its agents...")
        # Note: This loads the model twice. We will optimize this later.
        self.meta_agent = MetaAgent()
        self.coding_agent = CodingAgent()
        log.info("Orchestrator initialization complete.")

    def handle_request(self, user_input):
        log.info(f"Orchestrator received request: '{user_input}'")
        coding_keywords = ["code", "python", "function", "script", "algorithm"]
        if any(keyword in user_input.lower() for keyword in coding_keywords):
            log.info("Request routed to CodingAgent.")
            response = self.coding_agent.invoke(user_input)
        else:
            log.info("Request routed to MetaAgent.")
            response = self.meta_agent.invoke(user_input)
        log.info("Orchestrator processed request and received response.")
        return response