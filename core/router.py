# core/router.py

from tools.registry import TOOLS

def route(step: str):
    """
    Decide which tool to use for a given step.
    HARD RULES > heuristics > fallback
    """
    step_lower = step.lower()

    # 🚨 HARD RULE: README must always be read via file tool
    if "readme.md" in step_lower or "read readme" in step_lower:
        return {
            "tool": "read_file",
            "args": {"path": "README.md"}
        }

    # 🚨 HARD RULE: explicit file reads
    if "read" in step_lower and ".md" in step_lower:
        words = step_lower.split()
        for w in words:
            if w.endswith(".md"):
                return {
                    "tool": "read_file",
                    "args": {"path": w}
                }

    # 🌐 URL access (handled by web tool if exists)
    if step_lower.startswith("http"):
        return {
            "tool": "web_fetch",
            "args": {"url": step.strip()}
        }

    # 🧠 Heuristic fallback
    if "read" in step_lower or "open" in step_lower:
        return {
            "tool": "read_file",
            "args": {"path": "README.md"}
        }

    # ❌ Default: no unsafe shell
    return {
        "tool": None,
        "args": {}
    }
