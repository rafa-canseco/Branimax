import requests
from dotenv import load_dotenv
import os

load_dotenv()

MAKE_PROMUEVO = os.environ.get("MAKE_PROMUEVO")

async def write_lead(payload):
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(MAKE_PROMUEVO, json=payload,headers=headers)
    response.raise_for_status()
    return response