from core.llm import llm_complete

SYSTEM_PROMPT = """
You are an AI planner.

Rules:
- Use the MINIMUM number of steps required
- Do NOT include navigation or editor usage
- For informational goals, include:
  1. Read the required file
  2. Produce a final summary

Return steps as a numbered list.
"""


def plan(goal: str):
    response = llm_complete(SYSTEM_PROMPT, goal)
    steps = []

    for line in response.splitlines():
        if line.strip() and line[0].isdigit():
            steps.append(line.split(".", 1)[1].strip())

    return steps
