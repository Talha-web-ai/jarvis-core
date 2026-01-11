# core/executor.py

from rich.console import Console
from core.router import route
from tools.registry import TOOLS

console = Console()

class ExecutorAgent:
    def __init__(self):
        self.read_once = False  # 🔒 prevent repeated reads

    def execute(self, step: str) -> str:
        console.print(f"[bold cyan]→ Executor:[/bold cyan] {step}")

        tool, arg = route(step)

        # 🔒 READ README ONLY ONCE
        if tool == "read_file" and self.read_once:
            return "README already read. Skipping."

        if tool and tool in TOOLS:
            if tool == "read_file":
                self.read_once = True

            result = TOOLS[tool]["handler"](arg)
            return f"SUMMARY_SOURCE:\n{result}"

        return f"Acknowledged step: {step}"
