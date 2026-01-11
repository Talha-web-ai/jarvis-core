# tools/registry.py

TOOLS = {}

def register_tool(name: str, description: str, handler):
    TOOLS[name] = {
        "description": description,
        "handler": handler
    }

def get_tools_prompt():
    prompt = "Available tools:\n"
    for name, meta in TOOLS.items():
        prompt += f"- {name}: {meta['description']}\n"
    return prompt
