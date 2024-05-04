from pathlib import Path
from openai import OpenAI
import os
from decouple import config
import time
from functions.text_to_speech import convert_mp3_to_wav

os.environ["OPENAI_API_KEY"] =config("OPEN_AI_KEY")
OpenAI.api_key = config("OPEN_AI_KEY")
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
    wav_data = convert_mp3_to_wav(response.content)
    return wav_data


import requests
from decouple import config
from functions.querys_db import getVoice,getStability,getSimilarity,getStyle,getCompanyId
from pydub import AudioSegment
import io


ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


#CONVERT TEXT TO SPEECH
def speech_to_text_eleven(message,voice,stability,similarity,style):
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
            # Comentado porque se va a quitar después
            with open('elevenlabs_speech.mp3', 'wb') as f:
                 f.write(response.content)
            end_time = time.time()
            print(f"Tiempo total de ejecución de Eleven Labs Turbo: {end_time - start_time} segundos")
            return response.content
    except Exception as e:
        return

    #####

def convert_text_to_speech_multilingual(message,id):
    start_time = time.time()
    company_id = 1
    stability = 0.5
    similarity = 0.5
    style = 0.5
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

    voz = "5foAkxpX0K5wizIaF5vu"

    #Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json","accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/stream?optimize_streaming_latency=2"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
        if response.status_code == 200:
            with open('elevenlabs_speech_multilingual.mp3', 'wb') as f:
                f.write(response.content)
    except Exception as e:
        return
    end_time = time.time()
    print(f"Tiempo total de ejecución de Eleven Labs multilingual: {end_time - start_time} segundos")

def convert_text_to_speech_original(message,id):
    start_time = time.time()
    company_id = getCompanyId(id)
    stability = getStability(company_id)
    similarity = getSimilarity(company_id)
    style = getStyle(company_id)
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

    voz = getVoice(company_id)

    #Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json","accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voz}"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return
    end_time = time.time()
    print(f"Tiempo total de ejecución de Eleven Labs version original: {end_time - start_time} segundos")

# input_text = "esta es una muestra de audio para el avatar de inteligencia artificial"
# speech_to_text_openai(input_text)
# speech_to_text_eleven(input_text)
# convert_text_to_speech_multilingual(input_text,1)
# convert_text_to_speech_original(input_text,1)