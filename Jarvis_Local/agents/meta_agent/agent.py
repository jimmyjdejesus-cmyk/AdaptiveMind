from agents.base_agent.agent import BaseAgent

class MetaAgent(BaseAgent):
    def __init__(self):
        system_prompt = "You are J.A.R.V.I.S., a helpful and general-purpose AI assistant."
        super().__init__(system_prompt=system_prompt)