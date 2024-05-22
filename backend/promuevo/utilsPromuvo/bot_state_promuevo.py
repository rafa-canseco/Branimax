from typing import Dict, Any

class BotState:
    def __init__(self, initial_state: Dict[str, Any] = None):
        if initial_state is None:
            initial_state = {}
        self.state: Dict[str, Any] = initial_state

    def get(self, key: str, default=None):
        return self.state.get(key, default)

    def update(self, updates: Dict[str, Any]):
        self.state.update(updates)

    def clear(self):
        self.state.clear()
