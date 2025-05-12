import requests
from decouple import config
from functions.querys_db import getVoice,getStability,getSimilarity,getStyle,getCompanyId
from pydub import AudioSegment
import io


ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


#CONVERT TEXT TO SPEECH
def convert_text_to_speech(message,id):

    company_id = getCompanyId(id)
    stability = getStability(company_id)
    similarity = getSimilarity(company_id)
    style = getStyle(company_id)
    #Define Data
    body = {
        "text": message,
        "model_id": "eleven_multilingual_v1",
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

    voz = getVoice(company_id)

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
        mp3_data = response.content
        wav_data = convert_mp3_to_wav(mp3_data)
        return wav_data
    else:
        # Agregamos un print para ver la descripción del error
        print(f"Error: {response.status_code}, Descripción: {response.text}")
        return
    


def convert_mp3_to_wav(mp3_data):
    # Load mp3 data
    audio = AudioSegment.from_mp3(io.BytesIO(mp3_data))
    
    # Convert to wav
    wav_data = io.BytesIO()
    audio.export(wav_data, format="wav")
    wav_data.seek(0)
    print("exito convirtiendo audio")
    return wav_data.read()

def convert_text_to_speech_whatsapp(message):

    #Define Data
    body = {
        "text": message,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.06,
            "similarity_boost":0.3,
        }
    }

    voice_rachel = "XrExE9yKIg1WjnnlVkGX"



    #Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json","accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    # Send request
    try:
        print("generando voz")
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return
    
    #Handle Response 
    if response.status_code == 200:
        return response.content
    else:
        return
