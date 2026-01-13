# core/planner.py

from core.llm import llm_complete

SYSTEM_PROMPT = """
You are an AI planner.

Rules:
- Use AT MOST 2 steps
- For README or file summary tasks:
  1. Read the file
  2. Stop

Do NOT include extraction, rewriting, or refinement steps.

Return steps as a numbered list.
"""

def plan(goal: str):
    response = llm_complete(SYSTEM_PROMPT, goal)
    steps = []

    for line in response.splitlines():
        if line.strip() and line[0].isdigit():
            steps.append(line.split(".", 1)[1].strip())

    return steps
