from services.contextGlobal import get_context
import json

def  sellerFlow(body, user_data, id):
    chat_response = get_context(body, id, user_data)
    return chat_response