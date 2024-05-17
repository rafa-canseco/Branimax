# main.py
from utils.bot_state import BotState
from utils.history import handle_history, get_history, get_history_parse, clear_history
from services.aiService import AIClass
from flows.sellerFlow import sellerFlow
from flows.schedulerFlow import flow_schedule
from flows.confirmFlow import flow_confirm  
from functions.querys_db import get_state,update_state
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
import json

state = BotState()

PROMPT_DISCRIMINATOR = """### Historial de Conversación (Vendedor/Cliente) ###
{HISTORY}

### Intenciones del Usuario ###

**HABLAR**: Selecciona esta acción si el cliente parece querer hacer una pregunta o necesita más información.
**RESERVAR**: Selecciona esta acción si el cliente muestra intención de programar una cita.

### Instrucciones ###

Por favor, clasifica la siguiente conversación según la intención del usuario."""

async def mainMessaging(state: BotState, ai: AIClass, body: str,from_number):
    print(f"Estado actual de confirmation_phase: {state.get('confirmation_phase')}")
    if state.get('confirmation_phase'):
        response = await flow_confirm(state, ai, body,from_number)
        return response

    history = get_history_parse(state)
    print(history)
    prompt = PROMPT_DISCRIMINATOR.replace('{HISTORY}', history)

    prediction = await ai.determine_chat_fn([
        {"role": "system", "content": prompt}
    ])

    if "HABLAR" in prediction.get("prediction", ""):
        response = sellerFlow(body, state)
        return response
    elif "RESERVAR" in prediction.get("prediction", ""):
        response = await flow_schedule(state, ai, body)
        if "¿Confirmo tu reserva?" in response:
            state.update({'confirmation_phase': True})
            print("confirmation_phase actualizado a True")
        return response

async def register_message_and_process(body: str, state: BotState, ai: AIClass, from_number: str):
    handle_history({'role': 'user', 'content': body}, state)
    
    # Obtener el estado y el historial desde la base de datos
    state_dict, history, history_persistent = get_state(from_number)
    
    # Asegurarse de que state_dict sea un diccionario
    if isinstance(state_dict, str):
        state_dict = json.loads(state_dict)
    if isinstance(history, str):
        history = json.loads(history)
    if isinstance(history_persistent, str):
        history_persistent = json.loads(history_persistent)
    
    state.update(state_dict)
    handle_history({'role': 'user', 'content': body}, state)

    if not state.get('has_interacted'):
        welcome_message = "Hola! 👋 Soy Lina, tu asistente virtual 🤖. ¿En qué puedo ayudarte hoy? 😊✨"
        state.update({'has_interacted': True})
        update_state(from_number, state.state, get_history(state), history_persistent)
        return welcome_message
    
    response = await mainMessaging(state, ai, body, from_number)
    
    # Actualizar el historial persistente
    history_persistent.append({'role': 'user', 'content': body})
    history_persistent.append({'role': 'assistant', 'content': response})
    
    # Guardar el estado y el historial actualizado en la base de datos
    update_state(from_number, state.state, get_history(state), history_persistent)
    
    return response