from functions.querys_db import getPromtByCompany,getCompanyId
from utils.history import get_history_parse
from functions.openai_requests import get_chat_response_vectorized
import json


def get_context(message_input, id, user_data):

    history_str = get_history_parse(user_data)
    idCompany = getCompanyId(id)
    template = getPromtByCompany(idCompany)
    custom_template = template.format(HISTORY=history_str)
    chat_response = get_chat_response_vectorized(message_input,id,custom_template)
    print(chat_response)
    return chat_response