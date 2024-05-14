# main.py
from memory.bot_state import BotState
from memory.history import handle_history, get_history, get_history_parse, clear_history
from services.aiService import AIClass
##pendiente importar los flows
##pendiente importar las funcionalidades de AI
state = BotState()

PROMPT_DISCRIMINATOR = """### Historial de Conversación (Vendedor/Cliente) ###
{HISTORY}

### Intenciones del Usuario ###

**HABLAR**: Selecciona esta acción si el cliente parece querer hacer una pregunta o necesita más información.
**PROGRAMAR**: Selecciona esta acción si el cliente muestra intención de programar una cita.

### Instrucciones ###

Por favor, clasifica la siguiente conversación según la intención del usuario."""

async def mainMessaging(state: BotState,ai :AIClass):
    history =get_history_parse(state)
    prompt =PROMPT_DISCRIMINATOR.replace('{HISTORY}',history)

    prediction = await ai.determine_chat_fn([
        {"role": "system", "content": prompt}
    ])

    if "HABLAR" in prediction.get("prediction", ""):
        print("el usuario quiere hablar")
    if "RESERVAR" in prediction.get("prediction", ""):
        print("el usuario quiere programar")

async def register_message_and_process(body: str, state: BotState, ai: AIClass):
    handle_history({'role': 'user', 'content': body}, state)
    await mainMessaging(state, ai)