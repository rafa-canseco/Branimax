import requests
from decouple import config
import json
from supabase import create_client
from dotenv import load_dotenv
import os
load_dotenv()

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

url =os.environ.get("SUPABASE_URL")
key =os.environ.get("SUPABASE_KEY")
supabase=create_client(url,key)

#ELEVEN LABS
#CONVERT TEXT TO SPEECH
def convert_text_to_speech(message,id):

    #Define Data
    body = {
        "text": message,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost":0,
        }
    }

    voz_supabase = supabase.table("Particularities").select("voice").eq("id_company", id).execute()
    voz = voz_supabase.data[0]['voice']
    print(voz)
    #Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json","accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voz}"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return
    
    #Handle Response 
    if response.status_code == 200:
        return response.content
    else:
        return