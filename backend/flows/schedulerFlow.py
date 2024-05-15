from utils.currentDate import get_full_current_date
from utils.history import get_history_parse, handle_history
from services.getCalendar import get_current_calendar
from datetime import datetime, timedelta
from dateutil.parser import parse
from services.aiService import AIClass
from dateutil.relativedelta import relativedelta
import pytz

PROMPT_FILTER_DATE = """
### Contexto
Eres un asistente de inteligencia artificial. Tu propósito es determinar la fecha y hora que el cliente quiere, en el formato yyyy/MM/dd HH:mm:ss.

### Fecha y Hora Actual:
{CURRENT_DAY}

### Registro de Conversación:
{HISTORY}

Asistente: "{respuesta en formato (yyyy/MM/dd HH:mm:ss)}"
"""

DURATION_MEET = 45

def generate_prompt_filter(history) -> str:
    now_date = get_full_current_date()
    main_prompt = PROMPT_FILTER_DATE.replace('{HISTORY}', history).replace('{CURRENT_DAY}', now_date)
    return main_prompt

def is_within_interval(date, start, end):
    # Asegurarse de que todos los datetime sean offset-aware
    if start.tzinfo is None:
        start = start.replace(tzinfo=pytz.UTC)
    if end.tzinfo is None:
        end = end.replace(tzinfo=pytz.UTC)
    if date.tzinfo is None:
        date = date.replace(tzinfo=pytz.UTC)
    
    return start <= date <= end

async def flow_schedule(state, ai: AIClass,body):
    history = get_history_parse(state)
    list_ = get_current_calendar()

    list_parse = [
        {'from_date': parse(d), 'to_date': parse(d) + timedelta(minutes=DURATION_MEET)}
        for d in list_
    ]


    prompt_filter = generate_prompt_filter(history)
    response = await ai.desired_date_fn([{'role': 'system', 'content': prompt_filter}])
    desired_date = parse(response['date'])
    is_date_available = all(
        not is_within_interval(desired_date, item['from_date'], item['to_date'])
        for item in list_parse
    )

    print(f"Desired Date: {desired_date}")
    print(f"Is Date Available: {is_date_available}")
    if is_date_available is False:
        response = 'Lo siento, esa hora ya está reservada. ¿Alguna otra fecha y hora?'
        handle_history({'role': 'assistant', 'content': response}, state)
        state.clear()
        return response
    else:
        formatted_date_from = desired_date.strftime('%I:%M %p')
        formatted_date_to = (desired_date + timedelta(minutes=DURATION_MEET)).strftime('%I:%M %p')
        message = f"¡Perfecto! Tenemos disponibilidad de {formatted_date_from} a {formatted_date_to} el día {desired_date.strftime('%d/%m/%Y')}. ¿Confirmo tu reserva? *si*"
        handle_history({'content': message, 'role': 'assistant'}, state)
        state.update({'desiredDate': desired_date})
        return message
