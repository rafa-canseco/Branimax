from promuevo.utilsPromuvo.bot_state_promuevo import BotState
from promuevo.utilsPromuvo.historyPromuevo import (
    handle_history,
    get_history,
    get_history_parse
)
from promuevo.services.aiService import AIClassPromuevo
from functions.querys_db import get_state, update_state, get_discriminator_prompt
from promuevo.flows.sellerFlow import sellerFlow
from promuevo.flows.serviceFlow import serviceIdentifier
from promuevo.flows.recruitmentFlow import flow_recruit
import json


state = BotState()


async def register_message_and_process_promuevo(body: str, ai: AIClassPromuevo, from_number: str, database: str, id):
    state_dict, history, history_persistent = get_state(from_number, database)

    if isinstance(state_dict, str):
        state_dict = json.loads(state_dict)
    if isinstance(history_persistent, str):
        history_persistent = json.loads(history_persistent)

    state.update(state_dict)

    if not state.get('has_interacted') or state.get('reset_conversation'):
        welcome_message = "Hola! 👋 Soy David, tu asistente virtual 🤖. ¿En qué puedo ayudarte hoy? 😊✨"
        state.update({'has_interacted': True, 'reset_conversation': False})
        update_state(from_number, state.state, get_history(state), history_persistent, database)
        return welcome_message

    handle_history({"role": "user", "content": body}, state)

    response = await mainMessaging(state, ai, body, from_number, id, database)

    history_persistent.append({"role": "user", "content": body})
    history_persistent.append({"role": "assistant", "content": response})

    update_state(from_number, state.state, get_history(state), history_persistent, database)

    return response


async def mainMessaging(state: BotState, ai: AIClassPromuevo, body: str, from_number,id,database):
    print(f"Estado actual de recruitment_phase: {state.get('recruitment_phase')}")
    print(state)
    if state.get("recruitment_phase") is True:
        response = await flow_recruit(state, body, from_number, database)
        return response

    history = get_history_parse(state)
    PROMPT_DISCRIMINATOR = get_discriminator_prompt(id)
    prompt = PROMPT_DISCRIMINATOR.replace("{HISTORY}", history)

    prediction = await ai.determine_chat_fn([{"role": "system", "content": prompt}])

    if "HABLAR" in prediction.get("prediction", ""):
        response = sellerFlow(body, state,id)
        return response
    if "SERVICIOS" in prediction.get("prediction", ""):
        response = await serviceIdentifier(state, ai)
        return response
    if "RESERVAR" in prediction.get("prediction", ""):
        response = """Claro, con gusto te pongo en contacto con un asesor. Por favor, agenda una cita en el siguiente enlace de Calendly y estaremos encantados de atenderte:

                        https://calendly.com/promuevo/30min

                        ¡Esperamos hablar contigo pronto!"""
        return response
    if "TRABAJAR" in prediction.get("prediction", ""):
        state.update({"recruitment_phase": True})
        response = await flow_recruit(state, body, from_number, database)
        return response

    return
