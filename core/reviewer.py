# core/reviewer.py

from rich.console import Console

console = Console()

class ReviewerAgent:
    def review(self, result: str) -> bool:
        console.print(f"[bold magenta]→ Reviewer evaluating result[/bold magenta]")

        # Simple quality check (will become LLM-based later)
        if len(result) < 10:
            console.print("[red]✗ Result rejected[/red]")
            return False

        console.print("[green]✓ Result approved[/green]")
        return True
