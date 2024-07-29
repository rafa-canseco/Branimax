from typing import List, Dict, Union
import json

History = Dict[str, str]

def handle_history(inside: History, user_data: Dict):
    history = json.loads(user_data.get('history', '[]'))
    history.append(inside)
    return json.dumps(history)

def get_history(user_data: Dict, k: int = 15) -> List[History]:
    history = json.loads(user_data.get('history', '[]'))
    return history[-k:]

def get_history_parse(user_data: Union[Dict, List], k: int = 15) -> str:
    if isinstance(user_data, dict):
        history = json.loads(user_data.get('history', '[]'))
    elif isinstance(user_data, list):
        history = user_data
    else:
        raise ValueError("user_data debe ser un diccionario o una lista")
    
    limit_history = history[-k:]
    return ''.join(
        f'Customer: "{h["content"]}"' if h['role'] == 'user' else f'\nSeller: "{h["content"]}"\n'
        for h in limit_history
    )

def clear_history(user_data: Dict) -> Dict:
    user_data['history'] = '[]'
    return user_data