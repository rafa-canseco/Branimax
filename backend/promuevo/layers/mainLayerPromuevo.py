from promuevo.utilsPromuvo.bot_state_promuevo import BotState
from promuevo.utilsPromuvo.historyPromuevo import (
    handle_history,
    get_history,
    get_history_parse,
    clear_history,
)
from promuevo.services.aiService import AIClassPromuevo
from functions.querys_db import get_state, update_state
from promuevo.flows.sellerFlow import sellerFlow
from promuevo.flows.serviceFlow import serviceIdentifier
from promuevo.flows.recruitmentFlow import flow_recruit
import json


state = BotState()


PROMPT_DISCRIMINATOR = """### Historial de Conversación (Vendedor/Cliente) ###
{HISTORY}

### Intenciones del Usuario ###

**HABLAR**: Selecciona esta acción si el cliente parece querer hacer una pregunta o necesita más información sobre promuevo.
**SERVICIOS**: Selecciona esta acción si el cliente quiere conocer los servicios.
**RECLUTAR**: Selecciona esta acción si el cliente quiere trabajar con promuevo.
**RESERVAR**: Selecciona esta acción si el cliente muestra intención de programar una cita.

### Instrucciones ###

Por favor, clasifica la siguiente conversación según la intención del usuario."""


async def register_message_and_process_promuevo(
    body: str, state: BotState, ai: AIClassPromuevo, from_number: str, database: str
):
    handle_history({"role": "user", "content": body}, state)

    state_dict, history, history_persistent = get_state(from_number, database)

    if isinstance(state_dict, str):
        state_dict = json.loads(state_dict)
    if isinstance(history, str):
        history = json.loads(history)
    if isinstance(history_persistent, str):
        history_persistent = json.loads(history_persistent)

    state.update(state_dict)
    handle_history({"role": "user", "content": body}, state)

    response = await mainMessaging(state, ai, body, from_number)

    history_persistent.append({"role": "user", "content": body})
    history_persistent.append({"role": "assitant", "content": response})

    update_state(
        from_number, state.state, get_history(state), history_persistent, database
    )

    return response


async def mainMessaging(state: BotState, ai: AIClassPromuevo, body: str, from_number):

    print(f"Estado actual de recruitment_phase: {state.get('recruitment_phase')}")
    if state.get("recruitment_phase"):
        response = await flow_recruit(state, body,from_number)
        return response

    history = get_history_parse(state)
    prompt = PROMPT_DISCRIMINATOR.replace("{HISTORY}", history)

    prediction = await ai.determine_chat_fn([{"role": "system", "content": prompt}])

    if "HABLAR" in prediction.get("prediction", ""):
        response = sellerFlow(body, state)
        return response
    if "SERVICIOS" in prediction.get("prediction", ""):
        response = await serviceIdentifier(state, ai)
        return response
    if "RESERVAR" in prediction.get("prediction", ""):
        response = "LigaDeCalendly"
        return response
    if "RECLUTAR" in prediction.get("prediction", ""):
        response = await flow_recruit(state,body,from_number)
        return response

    return
