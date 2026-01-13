# tools/registry.py

from tools.file_tool import read_file
from tools.shell_tool import run_shell
from tools.web_tool import fetch_web

TOOLS = {
    "read_file": {
        "handler": read_file,
        "description": "Read contents of a local file"
    },
    "run_shell": {
        "handler": run_shell,
        "description": "Run safe shell commands (ls, pwd only)"
    },
    "fetch_web": {
        "handler": fetch_web,
        "description": "Fetch content from allowed web domains (read-only)"
    }
}

def get_tools_prompt():
    prompt = "Available tools:\n"
    for name, meta in TOOLS.items():
        prompt += f"- {name}: {meta['description']}\n"
    return prompt
