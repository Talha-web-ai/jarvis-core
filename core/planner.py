from core.llm import llm_complete

SYSTEM_PROMPT = """
You are an AI planner.
Break the user's goal into clear, ordered, executable steps.
Return steps as a numbered list.
"""

def plan(goal: str):
    response = llm_complete(SYSTEM_PROMPT, goal)
    steps = []

    for line in response.splitlines():
        if line.strip() and line[0].isdigit():
            steps.append(line.split(".", 1)[1].strip())

    return steps
