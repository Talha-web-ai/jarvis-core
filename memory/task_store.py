import json
import uuid
from pathlib import Path
from datetime import datetime

TASK_FILE = Path("memory/tasks.json")

class TaskStore:
    def __init__(self):
        TASK_FILE.parent.mkdir(exist_ok=True)
        if not TASK_FILE.exists():
            TASK_FILE.write_text("[]")

    def _load(self):
        return json.loads(TASK_FILE.read_text())

    def _save(self, tasks):
        TASK_FILE.write_text(json.dumps(tasks, indent=2))

    def create_task(self, goal, steps):
        tasks = self._load()
        task = {
            "id": str(uuid.uuid4()),
            "goal": goal,
            "steps": steps,
            "current_step": 0,
            "status": "in_progress",
            "results": [],
            "last_updated": datetime.utcnow().isoformat()
        }
        tasks.append(task)
        self._save(tasks)
        return task

    def update_task(self, task):
        tasks = self._load()
        for i, t in enumerate(tasks):
            if t["id"] == task["id"]:
                tasks[i] = task
                break
        self._save(tasks)

    def get_last_incomplete_task(self):
        tasks = self._load()
        for task in reversed(tasks):
            if task["status"] != "completed":
                return task
        return None
