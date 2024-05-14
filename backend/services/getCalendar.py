import requests
from dotenv import load_dotenv
import os

load_dotenv()

MAKE_GET_FROM_CALENDAR = os.environ.get("MAKE_GET_FROM_CALENDAR")
MAKE_ADD_TO_CALENDAR = os.environ.get("MAKE_ADD_TO_CALENDAR")

def get_current_calendar():

        response = requests.get(MAKE_GET_FROM_CALENDAR)
        response.raise_for_status()
        json_data = response.json()
        list_ = [item['date'] for item in json_data if item.get('date') and item.get('name')]
        return list_

async def add_to_calendar(payload):

        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(MAKE_ADD_TO_CALENDAR, json=payload, headers=headers)
        response.raise_for_status()
        return response

payload_example = {
    "name": "John Doe",
    "email": "johndoe@example.com", 
    "startDate": "2023-06-01",
    "phone": "+1234567890"
}


