from utils.currentDate import get_full_current_date
from utils.history import get_history_parse, handle_history
from services.getCalendar import get_current_calendar
from functions.querys_db import get_calendar_prompt
from datetime import datetime, timedelta
from dateutil.parser import parse
from services.aiService import AIClass
from dateutil.relativedelta import relativedelta
import pytz



DURATION_MEET = 60
TIMEZONE = "Etc/GMT+6"  # GMT-6

def generate_prompt_filter(history,id) -> str:
    now_date = get_full_current_date()
    PROMPT_FILTER_DATE = get_calendar_prompt(id)
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

async def flow_schedule(state, ai: AIClass, body,id):

    history = get_history_parse(state)
    list_ = get_current_calendar(id)


    # Normalizar las fechas en list_ al mismo formato y zona horaria
    local_tz = pytz.timezone(TIMEZONE)
    list_parse = []
    for d in list_:
        try:
            from_date = parse(d)
            if from_date.tzinfo is None:
                from_date = local_tz.localize(from_date)
            to_date = from_date + timedelta(minutes=DURATION_MEET)
            list_parse.append({'from_date': from_date, 'to_date': to_date})
        except Exception as e:
            print(f"Error parsing date {d}: {e}")

    prompt_filter = generate_prompt_filter(history,id)
    response = await ai.desired_date_fn([{'role': 'system', 'content': prompt_filter}])
    
    desired_date = parse(response['date'])
    if desired_date.tzinfo is None:
        desired_date = local_tz.localize(desired_date)
    
    is_date_available = all(
        not is_within_interval(desired_date, item['from_date'], item['to_date'])
        for item in list_parse
    )

    print(f"Desired Date: {desired_date}")
    print(f"Is Date Available: {is_date_available}")
    if not is_date_available:
        response = 'Lo siento 😔, esa hora ya está reservada. ¿Te gustaría elegir otra fecha y hora? 📅⏰'
        handle_history({'role': 'assistant', 'content': response}, state)
        state.clear()
        return response
    else:
        formatted_date_from = desired_date.strftime('%I:%M %p')
        formatted_date_to = (desired_date + timedelta(minutes=DURATION_MEET)).strftime('%I:%M %p')
        message = f"¡Perfecto! 🎉 Tenemos disponibilidad de {formatted_date_from} a {formatted_date_to} el día {desired_date.strftime('%d/%m/%Y')} 📅. ¿Confirmo tu reserva? 😊✨"
        handle_history({'content': message, 'role': 'assistant'}, state)
        state.update({'desiredDate': desired_date})
        return message