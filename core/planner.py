from core.llm import llm_complete
from core.cache import SimpleCache

cache = SimpleCache()

SYSTEM_PROMPT = """
You are an AI planner.

Rules:
- Use AT MOST 2 steps
- For README or file summary tasks:
  1. Read the file
  2. Stop

Do NOT include extraction, refinement, or rewriting steps.

Return steps as a numbered list.
"""


def plan(goal: str):
    cached = cache.get(goal)
    if cached:
        return cached

    response = llm_complete(SYSTEM_PROMPT, goal)
    steps = []

    for line in response.splitlines():
        if line.strip() and line[0].isdigit():
            steps.append(line.split(".", 1)[1].strip())

    cache.set(goal, steps)
    return steps
