import json
import os
from datetime import datetime
from difflib import SequenceMatcher

MEMORY_FILE = "memory_store.json"


class LongTermMemory:
    def __init__(self, path=MEMORY_FILE):
        self.path = path
        self._load()

    def _load(self):
        if not os.path.exists(self.path):
            self.memories = []
            return
        try:
            with open(self.path, "r") as f:
                self.memories = json.load(f)
        except Exception:
            self.memories = []

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.memories, f, indent=2)

    def add(self, content, confidence=0.8):
        if self.exists_similar(content):
            return  # 🚫 deduplication

        memory = {
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": confidence,
            "importance": confidence
        }

        self.memories.append(memory)
        self._save()

    def recall(self, query, min_confidence=0.6):
        matches = []

        for m in self.memories:
            similarity = SequenceMatcher(
                None, query.lower(), m["content"].lower()
            ).ratio()

            if similarity > 0.45 and m["confidence"] >= min_confidence:
                matches.append((similarity, m))

        matches.sort(reverse=True, key=lambda x: x[0])
        return [m for _, m in matches]

    def exists_similar(self, content, threshold=0.9):
        for m in self.memories:
            similarity = SequenceMatcher(
                None, content.lower(), m["content"].lower()
            ).ratio()
            if similarity >= threshold:
                return True
        return False
