#TODO:IF WORKS, create a new folder using this for the next bots
from promuevo.utilsPromuvo.bot_state_promuevo import BotState
from promuevo.utilsPromuvo.historyPromuevo import ( handle_history, get_history_parse)
from functions.querys_db import get_state,update_state
from services.aiService import AIClass
from services.contextGlobal import get_context

import json

state = BotState()

async def register_message_on_db(body: str,ai:AIClass, state: BotState , from_number:str,database:str,id):
    handle_history({"role": "user", "content": body}, state)

    state_dict, history, history_persistent = get_state(from_number, database)
    if isinstance(state_dict, str):
        state_dict = json.loads(state_dict)
    if isinstance(history, str):
        history = history
    if isinstance(history_persistent, str):
        history_persistent = json.loads(history_persistent)

    state.update(state_dict)
    handle_history({"role": "user", "content": body},state)

    response = await mainMessaging(state,ai,body=body,from_number=from_number,id=id)
    history_persistent.append({"role": "user","content": body})
    history_persistent.append({"role": "assitant", "content": response})

    update_state(from_number,state.state,get_history_parse(state),history_persistent,database)

    return response


async def mainMessaging(state:BotState, ai:AIClass,body:str,from_number,id):
    chat_response = get_context(body,id,state)
    handle_history({"role": "seller", "content": chat_response}, state)
    return chat_response



