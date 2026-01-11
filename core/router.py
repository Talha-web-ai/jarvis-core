# core/router.py

from core.llm import llm_complete
from core.cache import SimpleCache
from tools.registry import TOOLS, get_tools_prompt

route_cache = SimpleCache()

SYSTEM_PROMPT = """
You are a tool router for an autonomous AI agent.

Rules:
- Use read_file ONLY when reading file contents (e.g., README.md)
- Use run_shell ONLY for directory checks (ls, pwd, whoami)
- NEVER use shell commands to read files
- NEVER guess file paths
- NEVER leave ARG empty
- If no tool is required, return TOOL:NONE

Respond in EXACTLY one of these formats:

TOOL:<tool_name>
ARG:<argument>

OR

TOOL:NONE
"""

def route(step: str):
    step_lower = step.lower()

    cached = route_cache.get(step)
    if cached:
        return cached

    # 🔒 Heuristic shortcut
    if "readme" in step_lower or "summarize" in step_lower:
        decision = ("read_file", "README.md")
        route_cache.set(step, decision)
        return decision

    prompt = f"""
Task Step:
{step}

{get_tools_prompt()}
"""

    decision_text = llm_complete(SYSTEM_PROMPT, prompt)

    if not decision_text or not isinstance(decision_text, str):
        return None, None

    decision_text = decision_text.strip()

    if decision_text.startswith("TOOL:NONE"):
        route_cache.set(step, (None, None))
        return None, None

    lines = decision_text.splitlines()
    if len(lines) < 2:
        return None, None

    try:
        tool = lines[0].split(":", 1)[1].strip()
        arg = lines[1].split(":", 1)[1].strip()
    except Exception:
        return None, None

    if tool not in TOOLS:
        return None, None

    if not arg or arg.lower() in ["none", "null", ""]:
        return None, None

    route_cache.set(step, (tool, arg))
    return tool, arg
