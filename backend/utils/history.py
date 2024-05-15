from typing import List, Dict
from .bot_state import BotState

History = Dict[str, str]

def handle_history(inside: History, state: BotState):
    history = state.get('history', [])
    history.append(inside)
    state.update({'history': history})

def get_history(state: BotState, k: int = 15) -> List[History]:
    history = state.get('history', [])
    return history[-k:]

def get_history_parse(state: BotState, k: int = 15) -> str:
    history = state.get('history', [])
    limit_history = history[-k:]
    return ''.join(
        f'Customer: "{h["content"]}"' if h['role'] == 'user' else f'\nSeller: "{h["content"]}"\n'
        for h in limit_history
    )

def clear_history(state: BotState):
    state.clear()