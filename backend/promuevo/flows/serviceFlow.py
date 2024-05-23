from promuevo.services.aiService import AIClassPromuevo
from promuevo.utilsPromuvo.historyPromuevo import get_history_parse

PROMPT_IDENTIFY_SERVICE = """
### Contexto
Eres David, un asistente de la empresa Promuevo. propósito es identificar en qué servicio está interesado el cliente y proporcionarle un enlace al sitio web del servicio específico.

### Servicios Disponibles:
1. Consultoría de Negocios
2. Desarrollo de Software
3. Marketing Digital
4. Soporte Técnico
5. Diseño Gráfico

### Enlaces a Servicios:
1. Consultoría de Negocios: https://example.com/consultoria-de-negocios
2. Desarrollo de Software: https://example.com/desarrollo-de-software
3. Marketing Digital: https://example.com/marketing-digital
4. Soporte Técnico: https://example.com/soporte-tecnico
5. Diseño Gráfico: https://example.com/diseno-grafico

### Registro de Conversación:
{HISTORY}
"""

async def serviceIdentifier(state,ai:AIClassPromuevo):
    history = get_history_parse(state)
    prompt = PROMPT_IDENTIFY_SERVICE.replace('{HISTORY}',history)

    prediction = await ai.desired_service_fn([
        {"role": "system","content": prompt}
    ])

    service = prediction.get("prediction", "")

    if "Consultoría de Negocios" in service:
        url = "https://example.com/consultoria-de-negocios"
    elif "Desarrollo de Software" in service:
        url = "https://example.com/desarrollo-de-software"
    elif "Marketing Digital" in service:
        url = "https://example.com/marketing-digital"
    elif "Soporte Técnico" in service:
        url = "https://example.com/soporte-tecnico"
    elif "Diseño Gráfico" in service:
        url = "https://example.com/diseno-grafico"
    else:
        url = "https://example.com/servicios"

    response = f"El servicio que usted necesita es: {service}. Puede encontrar más información en el siguiente enlace: {url}"
    return response
