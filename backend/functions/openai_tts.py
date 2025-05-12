import requests
from functions.querys_db import getVoice,getStability,getSimilarity,getStyle,getCompanyId
from pydub import AudioSegment
import io
from pathlib import Path
from openai import OpenAI
import os
from decouple import config
import time
from functions.text_to_speech import convert_mp3_to_wav

os.environ["OPENAI_API_KEY"] =config("OPENAI_API_KEY")
OpenAI.api_key = config("OPENAI_API_KEY")
client = OpenAI()

def speech_to_text_openai(input_text,voice):
    start_time = time.time()
    speech_file_path = Path(__file__).parent /  "openai_speech.mp3"
    response = client.audio.speech.create(
      model="tts-1",
      voice=voice,
      input=input_text
    )
    response.stream_to_file(speech_file_path)
    end_time = time.time()
    print(f"Tiempo total de ejecución de OpenAI: {end_time - start_time} segundos")
    # Convertir el audio a formato wav
    # wav_data = convert_mp3_to_wav(response.content)
    return response.content




ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


#CONVERT TEXT TO SPEECH
def speech_to_text_eleven_turbo(message,voice,stability,similarity,style):
    start_time = time.time()

    #Define Data
    body = {
        "text": message,
        "model_id": "eleven_turbo_v2",
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

    #Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json","accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/stream?optimize_streaming_latency=3"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
        if response.status_code == 200:
            storage_path = Path(__file__).parent / "storage" / "elevenlabs_speech.mp3"
            storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(storage_path, 'wb') as f:
                f.write(response.content)
            end_time = time.time()
            print(f"Tiempo total de ejecución de Eleven Labs Turbo: {end_time - start_time} segundos")
            return response.content
    except Exception as e:
        return

    #####

def convert_text_to_speech_multilingual(message,voice,stability,similarity,style):
    start_time = time.time()
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


    #Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json","accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/stream?optimize_streaming_latency=2"

     # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return
    
    if response.status_code == 200:
        mp3_data = response.content
        wav_data = convert_mp3_to_wav(mp3_data)
        return wav_data
    else:
        # Agregamos un print para ver la descripción del error
        print(f"Error: {response.status_code}, Descripción: {response.text}")
        return

