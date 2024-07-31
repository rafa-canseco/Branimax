#TODO:IF WORKS, create a new folder using this for the next bots
from promuevo.utilsPromuvo.bot_state_promuevo import BotState
from promuevo.utilsPromuvo.historyPromuevo import ( handle_history, get_history_parse)
from functions.querys_db import get_state,update_state,get_user_data_vanquish,update_user_data
from services.aiService import AIClass
from services.contextGlobal import get_context

import json



async def register_message_on_db(body: str,ai:AIClass, from_number:str,database:str,id):
    user_data = get_user_data_vanquish(database, from_number)

    history = json.loads(user_data['history'])
    history.append({"role": "user", "content": body})

    response = await mainMessaging(user_data,body=body,from_number=from_number,id=id,database=database)
    history.append({"role": "assistant", "content": response})
    update_user_data(database, from_number, {'history': json.dumps(history)})

    return response


async def mainMessaging(user_data,body:str,from_number,id,database):
    user_data = get_user_data_vanquish(database, from_number)
    
    history = json.loads(user_data['history'])
    
    chat_response = get_context(body, id, user_data)
    
    history.append({"role": "assistant", "content": chat_response})
    update_user_data(database, from_number, {'history': json.dumps(history)})
    
    return chat_response



