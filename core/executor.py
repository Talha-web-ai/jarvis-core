# core/executor.py
from rich.console import Console
from core.router import route
from tools.registry import TOOLS

console = Console()

class ExecutorAgent:
    def execute(self, step: str) -> str:
        console.print(f"[bold cyan]→ Executor:[/bold cyan] {step}")

        tool, arg = route(step)

        if tool and tool in TOOLS:
            console.print(f"[yellow]Using tool:[/yellow] {tool}")
            result = TOOLS[tool]["handler"](arg)
            return f"Tool result: {result}"

        return f"No tool used. Step acknowledged: {step}"
