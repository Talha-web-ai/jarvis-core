# core/executor.py

from rich.console import Console

console = Console()

class ExecutorAgent:
    def execute(self, step: str) -> str:
        console.print(f"[bold cyan]→ Executor running:[/bold cyan] {step}")
        return f"Result of step: {step}"
