# core/agent.py

from rich.console import Console
from core.planner import plan
from core.executor import ExecutorAgent
from core.reviewer import ReviewerAgent
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory

console =j = Console()

class JarvisAgent:
    def __init__(self, goal: str, fast_mode: bool = True):
        self.goal = goal
        self.fast_mode = fast_mode
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
            result = self.executor.execute(step)

            # ⚡ FAST MODE: no reviewer, no retries
            if self.fast_mode:
                final_results.append(result)

                # 🛑 HARD STOP after summary
                if "summary" in result.lower():
                    return final_results

                continue

            # 🧐 Normal path with reviewer
            approved = self.reviewer.review(result)
            if approved:
                final_results.append(result)

                if "summary" in result.lower():
                    return final_results

        return final_results

    def run(self):
        self.think()
        return self.act()
