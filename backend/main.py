#uvicorn main:app
#comentario x
#Main Imports
from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

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

#Check Health
@app.get("/health")
async def checkHealth():
    return {"message": "Healthy"}

# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...)):

    # Convert audio to text - production
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)

    # Guard: Ensure output
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat response
    chat_response = get_chat_response(message_decoded)    

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")
    print(chat_response)
    
    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    # Guard: Ensure output
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed audio output")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Use for Post: Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

@app.post("/post-texto")
async def post_texto(data:dict):

    message_decoded = data["question"]
    print(message_decoded)
    #aqui hacer la petición a la base de datos dependiendo del id que mande del usuario
    response = get_chat_response(message_decoded)

    return {"response": response}
