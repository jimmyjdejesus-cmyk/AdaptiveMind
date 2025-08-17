import agent.tools as tools

class JanusAgent:
    def __init__(self, persona_prompt, tool_registry, approval_callback):
        self.persona_prompt = persona_prompt
        self.tools = tool_registry
        self.approval_callback = approval_callback

    def parse_natural_language(self, user_msg, uploaded_files):
        plan = []
        msg_lower = user_msg.lower()
        # File actions
        if uploaded_files and any(w in msg_lower for w in ["summarize", "analyze", "ingest", "read", "extract"]):
            filepaths = [f.name for f in uploaded_files]
            plan.append({"tool": "file_ingest", "args": {"files": [os.path.join("uploads", f) for f in filepaths]}})
        # Browser automation
        if "browse" in msg_lower or "go to" in msg_lower or "scrape" in msg_lower:
            # Extract URL -- very basic
            import re
            match = re.search(r"(https?://[^\s]+)", user_msg)
            actions = []
            if match:
                actions.append({"type": "goto", "url": match.group(1)})
            plan.append({"tool": "browser_automation", "args": {"actions": actions}})
        # Image generation
        if "image" in msg_lower or "picture" in msg_lower or "generate" in msg_lower:
            # Use the whole prompt as the image description
            plan.append({"tool": "image_generation", "args": {"prompt": user_msg}})
        # Default: just echo
        if not plan:
            plan.append({"tool": "echo", "args": {"message": "I'm not sure what you want. Try being more specific!"}})
        return plan

    def execute_plan(self, plan):
        results = []
        for step in plan:
            preview = self.tools.preview_tool_action(step)
            if not self.approval_callback(preview):
                results.append({"step": step, "result": "Denied by user"})
                continue
            result = self.tools.run_tool(step)
            results.append({"step": step, "result": result})
        return results