import agent.file_ingest as file_ingest
import agent.browser_automation as browser_automation
import agent.image_generation as image_generation

def preview_tool_action(step):
    return f"Will run {step['tool']} with args {step['args']}"



def run_tool(step):
    if step['tool'] == "file_ingest":
        return [file_ingest.ingest_file(f) for f in step['args'].get("files", [])]
    elif step['tool'] == "browser_automation":
        return browser_automation.automate_browser(step['args'].get("actions", []))
    elif step['tool'] == "image_generation":
        return image_generation.generate_image(step['args'].get("prompt", ""))
    elif step['tool'] == "echo":
        return step['args'].get("message", "")
    else:
        return None