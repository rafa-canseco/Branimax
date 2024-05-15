from utils.history import clear_history, handle_history
from services.getCalendar import add_to_calendar
from datetime import datetime, timedelta
from dateutil.parser import parse
import pytz


DURATION_MEET = 45
TIMEZONE = "Etc/GMT+6"  # GMT-6

async def flow_confirm(state, ai, body, from_number):
    if 'cancelar' in body.lower():
        clear_history(state)
        state.update({'confirmation_phase': False})  # Limpiar el estado de confirmación
        return "¿Cómo puedo ayudarte?"

    if not state.get('name'):
        if not state.get('name_prompted'):
            state.update({'name_prompted': True})
            return "Ok, voy a pedirte unos datos para agendar. ¿Cuál es tu nombre?"
        else:
            state.update({'name': body})
            state.update({'name_prompted': False})
            return "Última pregunta, ¿Cuál es tu email?"

    if not state.get('email'):
        if '@' not in body:
            return "Debes ingresar un email correcto"
        state.update({'email': body})
        
        desired_date = state.get('desiredDate')
        local_tz = pytz.timezone(TIMEZONE)
        start_dt = desired_date.astimezone(local_tz)
        end_dt = (desired_date + timedelta(minutes=DURATION_MEET)).astimezone(local_tz)

        date_object = {
            'name': state.get('name'),
            'email': state.get('email'),
            'start': {
                'dateTime': start_dt.isoformat()
            },
            'end': {
                'dateTime': end_dt.isoformat()
            },
            'phone': from_number
        }
        print(date_object)
        await add_to_calendar(date_object)
        clear_history(state)
        state.update({'confirmation_phase': False})  # Limpiar el estado de confirmación
        return "¡Listo! Agendado. Buen día."

    return "Ok, voy a pedirte unos datos para agendar. ¿Cuál es tu nombre?"