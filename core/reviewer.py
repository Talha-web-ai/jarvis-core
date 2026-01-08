# core/reviewer.py
from core.llm import llm_complete
from rich.console import Console

console = Console()

SYSTEM_PROMPT = """
You are a strict reviewer AI.
Approve results only if they are useful, correct, and clear.
Respond with APPROVE or REJECT and a short reason.
"""

class ReviewerAgent:
    def review(self, result: str) -> bool:
        feedback = llm_complete(SYSTEM_PROMPT, result)
        console.print(f"[bold magenta]→ Reviewer:[/bold magenta] {feedback}")
        return feedback.upper().startswith("APPROVE")
