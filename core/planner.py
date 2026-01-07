# core/planner.py

from typing import List

def plan(goal: str) -> List[str]:
    """
    Breaks a high-level goal into smaller executable steps.
    """
    steps = [
        f"Understand the goal: {goal}",
        "Identify required information",
        "Perform analysis or research",
        "Generate a clear, structured response"
    ]
    return steps
