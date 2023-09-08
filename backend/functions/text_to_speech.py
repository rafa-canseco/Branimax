import requests
from decouple import config
from functions.querys_db import getVoice,getStability,getSimilarity,getStyle

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


#CONVERT TEXT TO SPEECH
def convert_text_to_speech(message,id):

    stability = getStability(id)
    similarity = getSimilarity(id)
    style = getStyle(id)
    #Define Data
    body = {
        "text": message,
        "model_id": "eleven_multilingual_v2",
        "languages": [
        {
        "language_id": "es",
        "name": "Spanish"
        }],
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
        }
    }

    voz = getVoice(id)

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
        # Agregamos un print para ver la descripción del error
        print(f"Error: {response.status_code}, Descripción: {response.text}")
        return