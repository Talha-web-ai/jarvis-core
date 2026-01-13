# core/executor.py

from rich.console import Console
from core.router import route
from tools.registry import TOOLS
from tools.html_cleaner import html_to_text
from core.tool_evaluator import evaluate_tool_result

console = Console()

DOC_FALLBACKS = {
    "requests": "https://requests.readthedocs.io/en/latest/"
}

class ExecutorAgent:
    def __init__(self):
        self.read_once = False
        self.web_attempted = False

    def execute(self, step: str) -> str:
        console.print(f"[bold cyan]→ Executor:[/bold cyan] {step}")

        tool, arg = route(step)

        if tool == "read_file" and self.read_once:
            return "README already read. Skipping."

        if tool and tool in TOOLS:
            if tool == "read_file":
                self.read_once = True

            raw_result = TOOLS[tool]["handler"](arg)

            # 🌐 Web handling
            if tool == "fetch_web":
                if "404" in raw_result and not self.web_attempted:
                    self.web_attempted = True
                    for key, url in DOC_FALLBACKS.items():
                        if key in step.lower():
                            console.print(
                                f"[yellow]Retrying with official docs:[/yellow] {url}"
                            )
                            raw_result = TOOLS["fetch_web"]["handler"](url)

                raw_result = html_to_text(raw_result)

            evaluation = evaluate_tool_result(raw_result)

            # ❌ Failed
            if evaluation["status"] == "failed":
                return "RESULT_FAILED: Tool output unreliable."

            # ⚠️ Weak but usable
            if evaluation["status"] == "weak":
                return f"SUMMARY_SOURCE (LOW CONFIDENCE):\n{raw_result[:2000]}"

            # ✅ Success
            return f"SUMMARY_SOURCE:\n{raw_result[:4000]}"

        return f"Acknowledged step: {step}"
