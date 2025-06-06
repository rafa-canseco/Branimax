import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz

load_dotenv()

MAKE_GET_FROM_CALENDAR_19 = os.environ.get("MAKE_GET_FROM_CALENDAR_19")
MAKE_ADD_TO_CALENDAR_19 = os.environ.get("MAKE_ADD_TO_CALENDAR_19")
TIMEZONE = "Etc/GMT+6"  # GMT-6

def get_current_calendar(id):
    if id == 15:
        make_get_from_calendar = MAKE_GET_FROM_CALENDAR_19
    else:
        make_get_from_calendar = os.environ.get(f"MAKE_GET_FROM_CALENDAR_{id}")

    response = requests.get(make_get_from_calendar)
    response.raise_for_status()
    json_data = response.json()
    list_ = [item['date'] for item in json_data if item.get('date') and item.get('name')]
    return list_

async def add_to_calendar(payload):
    headers = {
        "Content-Type": "application/json",
    }
    # Convert the date to the correct timezone
    if 'date' in payload:
        local_tz = pytz.timezone(TIMEZONE)
        utc_dt = datetime.strptime(payload['date'], "%Y-%m-%dT%H:%M:%S")
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        # Format the date with timezone offset in RFC3339 format
        payload['date'] = local_dt.isoformat()

    response = requests.post(MAKE_ADD_TO_CALENDAR_19, json=payload, headers=headers)
    response.raise_for_status()
    return response