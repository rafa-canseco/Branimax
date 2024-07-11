from promuevo.utilsPromuvo.historyPromuevo import handle_history
from promuevo.utilsPromuvo.bot_state_promuevo import BotState
from services.contextGlobal import get_context


def sellerFlow(body:str,state:BotState,id):
    chat_response = get_context(body,id,state)
    handle_history({'role': 'seller', 'content':chat_response},state)
    return chat_response