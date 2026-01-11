# core/agent.py

from core.planner import plan
from core.executor import ExecutorAgent
from core.reviewer import ReviewerAgent
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from rich.console import Console

console = Console()

class JarvisAgent:
    def __init__(self, goal: str):
        self.goal = goal
        self.planner_steps = []
        self.executor = ExecutorAgent()
        self.reviewer = ReviewerAgent()
        self.short_memory = ShortTermMemory()
        self.long_memory = LongTermMemory()

    def think(self):
        console.print("[bold green]JARVIS planning...[/bold green]")
        self.planner_steps = plan(self.goal)

    def act(self):
        final_results = []

        for step in self.planner_steps:
            for attempt in range(2):  # retry once
                result = self.executor.execute(step)
                approved = self.reviewer.review(result)

                if "Tool result" in result or "summary" in result.lower():
                    self.short_memory.add(result)
                    self.long_memory.add(result)
                    final_results.append(result)


        return final_results


    def run(self):
        self.think()
        return self.act()
