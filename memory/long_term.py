# memory/long_term.py

import json
from pathlib import Path

MEMORY_FILE = Path("memory_store.json")

class LongTermMemory:
    def __init__(self):
        if not MEMORY_FILE.exists():
            MEMORY_FILE.write_text(json.dumps([]))

    def add(self, item: str):
        data = json.loads(MEMORY_FILE.read_text())
        data.append(item)
        MEMORY_FILE.write_text(json.dumps(data, indent=2))

    def get_all(self):
        return json.loads(MEMORY_FILE.read_text())
