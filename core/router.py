# core/router.py

import re
from core.llm import llm_complete
from tools.registry import TOOLS, get_tools_prompt

SYSTEM_PROMPT = """
You are a tool router for an autonomous AI agent.

Rules:
- Use fetch_web ONLY for reading documentation or articles
- NEVER browse links recursively
- NEVER fetch multiple URLs
- Use read_file for local files
- Use run_shell ONLY for ls or pwd
- If no tool is required, return TOOL:NONE

Respond EXACTLY in this format:

TOOL:<tool_name>
ARG:<argument>

OR

TOOL:NONE
"""

# 🔒 Robust URL extraction (FINAL)
URL_REGEX = re.compile(
    r"(https?://[^\s<>\]\)]+)",
    re.IGNORECASE
)

def route(step: str):
    step_lower = step.lower()

    # 📄 README shortcut
    if "readme" in step_lower:
        return "read_file", "README.md"

    # 🌐 Extract URL ANYWHERE in sentence
    match = URL_REGEX.search(step)
    if match:
        url = match.group(1).strip().rstrip(").,]")
        return "fetch_web", url

    # 🧠 LLM routing fallback
    prompt = f"""
Task Step:
{step}

{get_tools_prompt()}
"""

    decision = llm_complete(SYSTEM_PROMPT, prompt)

    if not decision or not isinstance(decision, str):
        return None, None

    if decision.startswith("TOOL:NONE"):
        return None, None

    try:
        lines = decision.splitlines()
        tool = lines[0].split(":", 1)[1].strip()
        arg = lines[1].split(":", 1)[1].strip()

        # Sanitize arg if it's a URL
        url_match = URL_REGEX.search(arg)
        if url_match:
            arg = url_match.group(1).strip()

        if tool not in TOOLS:
            return None, None

        return tool, arg

    except Exception:
        return None, None
