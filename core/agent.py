# core/agent.py

from core.planner import plan
from core.executor import execute
from rich.console import Console

console = Console()

class JarvisAgent:
    def __init__(self, goal: str):
        self.goal = goal
        self.steps = []

    def think(self):
        console.print("[bold green]JARVIS thinking...[/bold green]")
        self.steps = plan(self.goal)

    def act(self):
        results = []
        for step in self.steps:
            result = execute(step)
            results.append(result)
        return results

    def run(self):
        self.think()
        results = self.act()
        return results
