# main.py

import sys
from rich.console import Console

from core.agent import JarvisAgent
from memory.task_store import TaskStore

console = Console()

def main():
    if len(sys.argv) < 2:
        console.print("[red]Please provide a goal for JARVIS[/red]")
        return

    goal = sys.argv[1].strip().lower()
    store = TaskStore()

    # 🔁 CONTINUE LAST TASK
    if goal in ["continue", "continue last task"]:
        task = store.get_last_incomplete_task()
        if not task:
            console.print("[yellow]No incomplete task found.[/yellow]")
            return

        console.print(f"[bold green]Continuing task:[/bold green] {task['goal']}")
        agent = JarvisAgent(task["goal"], fast_mode=True)
        agent.task = task
        agent.planner_steps = task["steps"]
        results = agent.act()

    else:
        agent = JarvisAgent(sys.argv[1], fast_mode=True)
        results = agent.run()

    if not results:
        console.print("[yellow]No meaningful output produced.[/yellow]")
        return

    # Deterministic final output (no LLM)
    for r in results:
        if "summary" in r.lower() or r.startswith("#"):
            console.print("\n[bold cyan]Final Answer:[/bold cyan]")
            console.print(r)
            return

    console.print("\n[bold cyan]Final Answer:[/bold cyan]")
    console.print(results[-1])


if __name__ == "__main__":
    main()
