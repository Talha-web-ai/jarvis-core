# memory/short_term.py

class ShortTermMemory:
    def __init__(self):
        self.data = []

    def add(self, item: str):
        self.data.append(item)

    def get_all(self):
        return self.data
