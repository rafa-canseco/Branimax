from promuevo.services.context import get_context
from promuevo.utilsPromuvo.historyPromuevo import handle_history
from promuevo.utilsPromuvo.bot_state_promuevo import BotState

id = 9

def sellerFlow(body:str,state:BotState):
    chat_response = get_context(body,id,state)
    handle_history({'role': 'seller', 'content':chat_response},state)
    return chat_response