from agents.base_agent.agent import BaseAgent

# This prompt could benefit from abstracting the language to a variable, e.g. `programming_language` 

class CodingAgent(BaseAgent):
    def __init__(self):
        system_prompt = (
            "You are an expert Python programmer. Your task is to provide clean, "
            "efficient, and correct code. Always wrap your code in ```python ... ``` blocks."
        )
        super().__init__(system_prompt=system_prompt)