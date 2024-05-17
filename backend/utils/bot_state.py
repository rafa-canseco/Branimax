from typing import Dict, Any

class BotState:
    def __init__(self, initial_state: Dict[str, Any] = None):
        if initial_state is None:
            initial_state = {}
        self.state: Dict[str, Any] = initial_state
        if 'has_interacted' not in self.state:
            self.state['has_interacted'] = False

    def get(self, key: str, default=None):
        return self.state.get(key, default)

    def update(self, updates: Dict[str, Any]):
        self.state.update(updates)

    def clear(self):
        # Preservar ciertos campos
        preserved_fields = {key: self.state[key] for key in ['has_interacted'] if key in self.state}
        self.state.clear()
        self.state.update(preserved_fields)