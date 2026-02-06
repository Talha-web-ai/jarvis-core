from core.router import route


class ExecutorAgent:
    def __init__(self):
        pass

    def run(self, step: str):
        """
        Execute a single step using tool routing.
        """
        return route(step)


# ✅ FUNCTION EXPORT (THIS FIXES YOUR ERROR)
def execute(step: str):
    executor = ExecutorAgent()
    return executor.run(step)
