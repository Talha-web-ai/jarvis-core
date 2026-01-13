# core/planner.py

from core.llm import llm_complete

SYSTEM_PROMPT = """
You are an AI planner.

Rules:
- Use AT MOST 3 steps
- If external information is required, include ONE web reading step
- NEVER include more than one web step
- Stop once information is gathered

Return steps as a numbered list.
"""

def plan(goal: str):
    response = llm_complete(SYSTEM_PROMPT, goal)
    steps = []

    for line in response.splitlines():
        if line.strip() and line[0].isdigit():
            steps.append(line.split(".", 1)[1].strip())

    return steps
