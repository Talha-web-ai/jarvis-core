# main.py

import sys
from rich.console import Console
from core.agent import JarvisAgent

console = Console()

def main():
    if len(sys.argv) < 2:
        console.print("[red]Please provide a goal for JARVIS[/red]")
        return

    goal = sys.argv[1]
    agent = JarvisAgent(goal, fast_mode=True)

    console.print("[bold green]JARVIS planning...[/bold green]")
    results = agent.run()

    if not results:
        console.print("[yellow]No meaningful output produced.[/yellow]")
        return

    # 🔒 README summarization = NO LLM
    for r in results:
        if r.startswith("SUMMARY_SOURCE"):
            content = r.replace("SUMMARY_SOURCE:", "").strip()

            # Simple, deterministic summary
            lines = content.splitlines()
            summary = "\n".join(lines[:15])  # top 15 lines

            console.print("\n[bold cyan]Final Answer:[/bold cyan]")
            console.print(summary)
            return

    # Fallback
    console.print("\n[bold cyan]Final Answer:[/bold cyan]")
    console.print(results[-1])


if __name__ == "__main__":
    main()
