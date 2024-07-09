from promuevo.services.aiService import AIClassPromuevo
from promuevo.utilsPromuvo.historyPromuevo import get_history_parse

PROMPT_IDENTIFY_SERVICE = """
### Contexto
Eres David, un asistente de la empresa Promuevo. propósito es identificar en qué servicio está interesado el cliente y proporcionarle un enlace al sitio web del servicio específico.

### Servicios Disponibles:
1.-Promotoría: Selecciona esta acción si el usuario pregunta por el servicio de promotoría o información sobre la ejecución en el punto de venta.
2.-Degustación & Demostración: Selecciona esta acción si el usuario pregunta por el servicio de degustación y demostración o información sobre la experiencia directa del producto.
3.-Software de Gestión en PDV: Selecciona esta acción si el usuario pregunta por el software de gestión en PDV o información sobre la optimización de la administración y control de puntos de venta.
4.-Trademarketing: Selecciona esta acción si el usuario pregunta por el servicio de trademarketing o información sobre estrategias para mejorar la presencia de la marca en el punto de venta.
5.-Gestión de herramientas: Selecciona esta acción si el usuario pregunta por la gestión de herramientas o información sobre la maximización de la eficiencia mediante el acceso a las mejores herramientas.
6.-Investigación del consumidor: Selecciona esta acción si el usuario pregunta por la investigación del consumidor o información sobre estudios para entender mejor a los consumidores y mejorar las estrategias de marketing.

### Enlaces a Servicios:
Promotoría: https://2promuevo.vercel.app/promotoria
Degustación & Demostración: https://2promuevo.vercel.app/degustacion&demostracion 
Software de Gestión en PDV: https://2promuevo.vercel.app/software 
Trademarketing: https://2promuevo.vercel.app/trademarketing 
Gestión decherramientas: https://2promuevo.vercel.app/gestion
Investigación del consumidor: https://2promuevo.vercel.app/investigacion

### Registro de Conversación:
{HISTORY}
"""

async def serviceIdentifier(state, ai: AIClassPromuevo):
    history = get_history_parse(state)
    prompt = PROMPT_IDENTIFY_SERVICE.replace('{HISTORY}', history)

    prediction = await ai.desired_service_fn([
        {"role": "system", "content": prompt}
    ])

    service = prediction.get("prediction", "")

    if "Promotoría" in service:
        url = "https://promuevo.mx/promotoria"
    elif "Degustación & Demostración" in service:
        url = "https://promuevo.mx/degustacion-demostracion"
    elif "Software de Gestión en PDV" in service:
        url = "https://promuevo.mx/software-pdv"
    elif "Trademarketing" in service:
        url = "https://promuevo.mx/trademarketing"
    elif "Gestión de herramientas" in service:
        url = "https://promuevo.mx/gestion-herramientas"
    elif "Investigación del consumidor" in service:
        url = "https://promuevo.mx/investigacion-comprador"
    else:
        response = (
            "Nuestros servicios son:\n"
            "1. Promotoría\n"
            "2. Degustación & Demostración\n"
            "3. Software de Gestión en PDV\n"
            "4. Trademarketing\n"
            "5. Gestión de herramientas\n"
            "6. Investigación del consumidor\n"
            "Entra a la siguiente liga para más información: https://promuevo.mx/servicios"
        )
        return response

    response = f"El servicio que usted necesita es: {service}. Puede encontrar más información en el siguiente enlace: {url}"
    return response
