from promuevo.services.aiService import AIClassPromuevo
from functions.querys_db import get_discriminator_prompt, update_user_data, get_user_data
from promuevo.flows.sellerFlow import sellerFlow
from promuevo.flows.serviceFlow import serviceIdentifier
from promuevo.flows.recruitmentFlow import flow_recruit

import json

async def register_message_and_process_promuevo(body: str, ai: AIClassPromuevo, from_number: str, database: str, id):
    user_data = get_user_data(database, from_number)

    if not user_data['has_interacted']:
        welcome_message = "Hola! 👋 Soy David, tu asistente virtual 🤖. ¿En qué puedo ayudarte hoy? 😊✨"
        update_user_data(database, from_number, {'has_interacted': True})
        return welcome_message
    
    history = json.loads(user_data['history'])
    history.append({"role": "user", "content": body})

    response = await mainMessaging(user_data, ai, body, from_number, id, database)

    # Solo actualizamos el historial si no se ha reiniciado el estado
    if not response.startswith("Proceso de reclutamiento finalizado"):
        history.append({"role": "assistant", "content": response})
        update_user_data(database, from_number, {'history': json.dumps(history)})

    return response

async def mainMessaging(user_data, ai: AIClassPromuevo, body: str, user_id, id, database):
    # Obtener los datos más recientes del usuario
    user_data = get_user_data(database, user_id)
    
    print(f"Estado actual de recruitment_phase: {user_data['recruitment_phase']}")
    if user_data['recruitment_phase']:
        response = await flow_recruit(user_data, body, user_id, database)
        return response  # Retornamos la respuesta inmediatamente si estamos en fase de reclutamiento

    history = json.loads(user_data['history'])
    PROMPT_DISCRIMINATOR = get_discriminator_prompt(id)
    prompt = PROMPT_DISCRIMINATOR.replace("{HISTORY}", json.dumps(history))

    prediction = await ai.determine_chat_fn([{"role": "system", "content": prompt}])

    if "HABLAR" in prediction.get("prediction", ""):
        response = sellerFlow(body, user_data, id)
    elif "SERVICIOS" in prediction.get("prediction", ""):
        response = await serviceIdentifier(user_data, ai)
    elif "RESERVAR" in prediction.get("prediction", ""):
        response = """Claro, con gusto te pongo en contacto con un asesor. Por favor, agenda una cita en el siguiente enlace de Calendly y estaremos encantados de atenderte:

                        https://calendly.com/promuevo/30min

                        ¡Esperamos hablar contigo pronto!"""
    elif "TRABAJAR" in prediction.get("prediction", ""):
        update_user_data(database, user_id, {'recruitment_phase': True})
        user_data['recruitment_phase'] = True
        response = await flow_recruit(user_data, body, user_id, database)
    else:
        response = "Lo siento, no entendí tu solicitud. ¿Podrías reformularla?"

    return response