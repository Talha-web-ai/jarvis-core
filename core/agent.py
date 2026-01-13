# core/agent.py

from rich.console import Console
from datetime import datetime

from core.planner import plan
from core.executor import ExecutorAgent
from memory.task_store import TaskStore

console = Console()

class JarvisAgent:
    def __init__(self, goal: str, fast_mode: bool = True):
        self.goal = goal
        self.fast_mode = fast_mode

        self.executor = ExecutorAgent()
        self.task_store = TaskStore()

        self.task = None
        self.planner_steps = []

    def think(self):
        console.print("[bold green]JARVIS planning...[/bold green]")
        self.planner_steps = plan(self.goal)
        self.task = self.task_store.create_task(self.goal, self.planner_steps)

    def act(self):
        final_results = []

        for i in range(self.task["current_step"], len(self.task["steps"])):
            step = self.task["steps"][i]
            result = self.executor.execute(step)

            final_results.append(result)
            self.task["results"].append(result)
            self.task["current_step"] = i + 1
            self.task["last_updated"] = datetime.utcnow().isoformat()

            # ❌ Tool failed
            if "RESULT_FAILED" in result:
                self.task["status"] = "failed"
                self.task_store.update_task(self.task)
                return final_results

            # ⚠️ Low confidence result
            if "LOW CONFIDENCE" in result:
                self.task["status"] = "completed_with_low_confidence"
                self.task_store.update_task(self.task)
                return final_results

            # ✅ Normal completion
            if "SUMMARY_SOURCE" in result:
                self.task["status"] = "completed"
                self.task_store.update_task(self.task)
                return final_results

            self.task_store.update_task(self.task)

        self.task["status"] = "completed"
        self.task_store.update_task(self.task)
        return final_results

    def run(self):
        self.think()
        return self.act()
