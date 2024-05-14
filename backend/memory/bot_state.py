
from typing import List, Dict, Any

class BotState:
    def __init__(self):
        self.state: Dict[str, Any] = {}

    def get(self, key: str, default=None):
        return self.state.get(key, default)

    def update(self, updates: Dict[str, Any]):
        self.state.update(updates)

    def clear(self):
        self.state.clear()