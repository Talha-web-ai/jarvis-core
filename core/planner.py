# core/planner.py

from core.llm import llm_complete

SYSTEM_PROMPT = """
You are JARVIS, an autonomous AI planner.
Break the user goal into clear, minimal, executable steps.
Return steps as a numbered list.
"""


def plan(goal: str, memory_context: str = ""):
    prompt = goal

    if memory_context:
        prompt = f"""
Relevant past knowledge:
{memory_context}

Current goal:
{goal}
"""

    response = llm_complete(SYSTEM_PROMPT, prompt)

    steps = []
    for line in response.splitlines():
        if line.strip() and line[0].isdigit():
            steps.append(line.split(".", 1)[1].strip())

    return steps
