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

    raw_goal = sys.argv[1].strip()
    goal = raw_goal.lower()
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
        agent = JarvisAgent(raw_goal, fast_mode=True)
        results = agent.run()

    if not results:
        console.print("[yellow]No meaningful output produced.[/yellow]")
        return

    final = results[-1]

    console.print("\n[bold cyan]Final Answer:[/bold cyan]")

    if "LOW CONFIDENCE" in final:
        console.print("[yellow]⚠️ Result has low confidence[/yellow]")

    if "RESULT_FAILED" in final:
        console.print("[red]❌ Task failed due to unreliable data[/red]")

    console.print(final)


if __name__ == "__main__":
    main()
