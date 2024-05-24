import requests
import time
import json
from dotenv import load_dotenv
import os
load_dotenv()
TAVUS_API_KEY = os.getenv("TAVUS_API_KEY")

def crear_video(script, video_name):
    print(script)
    print(video_name)
    url = "https://tavusapi.com/v2/videos"
    payload = {
        "replica_id": "r660c4f3ba",
        "script": script,
        "video_name": "Testing"
    }
    headers = {
        "x-api-key": TAVUS_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        if response.status_code == 200:
            try:
                response_data = json.loads(response.text)
                print("Respuesta del servidor:", response_data)
                return response_data.get("video_id")
            except json.JSONDecodeError:
                print("Error decodificando JSON:", response.text)
                return None
        else:
            print("Error en la solicitud HTTP:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Error en la solicitud:", str(e))
        return None

def obtener_video(video_id):
    url = f"https://tavusapi.com/v2/videos/{video_id}"
    headers = {"x-api-key": TAVUS_API_KEY}
    while True:
        response = requests.get(url, headers=headers)
        response_data = json.loads(response.text)
        status = response_data.get("status")
        if status == "ready":
            download_url = response_data.get("download_url")
            stream_url = response_data.get("stream_url")
            return download_url, stream_url
        elif status == "generating" or status == "queued":
            time.sleep(5)
            print("Esperando la generación del video:", status)
        else:
            raise Exception(f"Estado inesperado: {status}")

def procesar_video(script,video_name):
    inicio = time.time()
    video_id = crear_video(script,video_name)
    download_url, stream_url = obtener_video(video_id)
    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(f"Download URL: {download_url}")
    print(f"Stream URL: {stream_url}")
    print(f"Tiempo total de procesamiento: {tiempo_transcurrido:.2f} segundos")
    return download_url, stream_url

