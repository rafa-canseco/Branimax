# main.py
from utils.bot_state import BotState
from utils.history import handle_history, get_history, get_history_parse, clear_history
from services.aiService import AIClass
from flows.sellerFlow import sellerFlow
from flows.schedulerFlow import flow_schedule
from flows.confirmFlow import flow_confirm  # Importar el flujo de confirmación

state = BotState()

state_cache = {}

def get_state(from_number):
    if from_number in state_cache:
        return state_cache[from_number]
    else:
        return BotState()

def update_state(from_number, state):
    state_cache[from_number] = state

PROMPT_DISCRIMINATOR = """### Historial de Conversación (Vendedor/Cliente) ###
{HISTORY}

### Intenciones del Usuario ###

**HABLAR**: Selecciona esta acción si el cliente parece querer hacer una pregunta o necesita más información.
**RESERVAR**: Selecciona esta acción si el cliente muestra intención de programar una cita.

### Instrucciones ###

Por favor, clasifica la siguiente conversación según la intención del usuario."""

async def mainMessaging(state: BotState, ai: AIClass, body: str, from_number):
    print(f"Estado actual de confirmation_phase: {state.get('confirmation_phase')}")
    
    if state.get('confirmation_phase'):
        response = await flow_confirm(state, ai, body, from_number)
        return response

    history = get_history_parse(state)
    print(f"Historial: {history}")
    prompt = PROMPT_DISCRIMINATOR.replace('{HISTORY}', history)

    prediction = await ai.determine_chat_fn([
        {"role": "system", "content": prompt}
    ])

    print(f"Predicción: {prediction.get('prediction', '')}")

    if "HABLAR" in prediction.get("prediction", ""):
        response = sellerFlow(body, state)
        return response
    elif "RESERVAR" in prediction.get("prediction", ""):
        response = await flow_schedule(state, ai, body)
        if "¿Confirmo tu reserva?" in response:
            state.update({'confirmation_phase': True})
            print("confirmation_phase actualizado a True")
        return response

async def register_message_and_process(body: str, state: BotState, ai: AIClass, from_number):
    handle_history({'role': 'user', 'content': body}, state)

    response = await mainMessaging(state, ai, body, from_number)
    update_state(from_number, state)  # Asegúrate de actualizar el estado después de procesar el mensaje
    return response