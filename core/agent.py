from core.planner import plan
from core.executor import execute
from core.reviewer import review
from memory.long_term import LongTermMemory


class JarvisAgent:
    def __init__(self, goal: str, fast_mode: bool = False):
        self.goal = goal
        self.fast_mode = fast_mode
        self.long_term_memory = LongTermMemory()

    def run(self):
        # 🔁 MEMORY RECALL FIRST
        recalled = self.long_term_memory.recall(
            self.goal,
            min_confidence=0.75
        )

        if recalled:
            return recalled[0]["content"]

        steps = plan(self.goal)
        results = []

        for step in steps:
            output = execute(step)

            if not output:
                continue

            # 🚀 FAST MODE SKIPS REVIEW
            if not self.fast_mode:
                verdict = review(output if isinstance(output, str) else str(output))
                if verdict != "APPROVE":
                    continue

            # ✅ NORMALIZE OUTPUT
            text = None

            if isinstance(output, str):
                text = output
            elif isinstance(output, dict):
                text = output.get("result") or output.get("content")

            if text:
                results.append(text)

        final_output = "\n\n".join(results)

        if final_output.strip():
            self.long_term_memory.add(
                content=final_output,
                confidence=0.8
            )

        return final_output
