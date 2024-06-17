from services.contextGlobal import get_context
from utils.history import handle_history
from utils.bot_state import BotState


def sellerFlow(body: str, state: BotState,id):
    chat_response = get_context(body, id, state)
    handle_history({'role': 'seller', 'content': chat_response}, state)
    return chat_response