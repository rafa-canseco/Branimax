from datetime import datetime
import locale

def get_full_current_date() -> str:
    # Establecer la localización para obtener el día de la semana en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    
    # Obtener la fecha y hora actual
    current_d = datetime.now()
    
    # Formatear la fecha y hora
    format_date = current_d.strftime('%Y/%m/%d %H:%M')
    
    # Obtener el día de la semana
    day = current_d.strftime('%A')
    
    # Devolver la fecha formateada y el día de la semana
    return f"{format_date} {day}"

