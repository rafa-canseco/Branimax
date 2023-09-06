#uvicorn main:app
#comentario x
#Main Imports
from fastapi import FastAPI,File,UploadFile,HTTPException,Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
import os
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()

#Custom Function Imports
from functions.openai_requests import convert_audio_to_text,get_chat_response
from functions.database import store_messages
from functions.text_to_speech import convert_text_to_speech

#Initiate App
app = FastAPI()

#CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]

#CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

url =os.environ.get("SUPABASE_URL")
key =os.environ.get("SUPABASE_KEY")
supabase=create_client(url,key)



#Check Health
@app.get("/health")
async def checkHealth():
    return {"message": "Healthy"}

# Post bot response


@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...), id: str = Form(...)):

    # Convert audio to text - production
    # Save the file temporarily
    print("id identificado:",id)
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())
    audio_input = open(file.filename, "rb")

    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)

    # Guardia: Asegurar salida
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Falló al decodificar audio")

    # Obtener respuesta del chat
    chat_response = get_chat_response(message_decoded, id)    

    # Guardia: Asegurar salida
    if not chat_response:
        raise HTTPException(status_code=400, detail="Falló la respuesta del chat")
    print(chat_response)
    
    # Convertir respuesta del chat a audio
    audio_output = convert_text_to_speech(chat_response,id)

    # Guardia: Asegurar salida
    if not audio_output:
        raise HTTPException(status_code=400, detail="Falló la salida de audio")

    # Crear un generador que produce fragmentos de datos
    def iterfile():
        yield audio_output

    # Usar para Post: Devolver audio de salida
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

@app.post("/post-texto")
async def post_texto(data:dict):

    message_decoded = data["question"]
    id = data["id"]
    print(message_decoded)
    print("id identificado:",id)
    #aqui hacer la petición a la base de datos dependiendo del id que mande del usuario
    response = get_chat_response(message_decoded,id)

    return {"response": response}
