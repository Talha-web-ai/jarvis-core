# main.py

import sys
from core.agent import JarvisAgent
from rich.console import Console

console = Console()

def main():
    if len(sys.argv) < 2:
        console.print("[red]Please provide a goal for JARVIS[/red]")
        return

    goal = sys.argv[1]
    agent = JarvisAgent(goal)
    results = agent.run()

    console.print("\n[bold yellow]Final Output:[/bold yellow]")
    for r in results:
        console.print(f"- {r}")

if __name__ == "__main__":
    main()
