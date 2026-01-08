# core/router.py

from core.llm import llm_complete
from tools.registry import TOOLS, get_tools_prompt

SYSTEM_PROMPT = """
You are a tool router for an autonomous AI agent.

Your task:
- Decide if a tool is REQUIRED to complete the step.
- Choose the MOST appropriate tool.
- Provide the REQUIRED argument.

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
    """
    Decide which tool to use (if any) for a given step.
    Returns (tool_name, argument) or (None, None).
    """

    step_lower = step.lower()

    # ---------- HEURISTIC SHORT-CIRCUITS (IMPORTANT) ----------

    # Direct README handling (prevents shell misuse & loops)
    if "readme" in step_lower or "summarize" in step_lower:
        return "read_file", "README.md"

    # ---------- LLM-BASED ROUTING ----------

    prompt = f"""
Task Step:
{step}

{get_tools_prompt()}
"""

    decision = llm_complete(SYSTEM_PROMPT, prompt)

    if not decision or not isinstance(decision, str):
        return None, None

    decision = decision.strip()

    # No tool required
    if decision.startswith("TOOL:NONE"):
        return None, None

    lines = decision.splitlines()
    if len(lines) < 2:
        return None, None

    # Parse tool and argument
    try:
        tool = lines[0].split(":", 1)[1].strip()
        arg = lines[1].split(":", 1)[1].strip()
    except Exception:
        return None, None

    # Validate tool
    if tool not in TOOLS:
        return None, None

    # Validate argument
    if not arg or arg.lower() in ["none", "null", ""]:
        return None, None

    return tool, arg
