#uvicorn main:app

#Main Imports
from fastapi import FastAPI,File,UploadFile,HTTPException,Form,Request
from fastapi.responses import StreamingResponse,JSONResponse,Response,FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from gotrue.errors import AuthApiError
import os
from supabase import create_client
import time
import requests
from dotenv import load_dotenv
from pydub import AudioSegment
from pydantic import BaseModel

#Custom Function Imports
from functions.openai_requests import convert_audio_to_text,get_chat_response,getResumeNote
from functions.text_to_speech import convert_text_to_speech_whatsapp
from functions.analisis import found_topics,scheme_topics,generate_question,get_resume_users,get_info_users
from functions.querys_db import conversation_by_user,getCompanyId,getVoiceSource,getExactVoice,getSimilarity,getStyle,getStability,delete_state
from functions.openai_tts import speech_to_text_openai,convert_text_to_speech_multilingual
from functions.tavus_requests import procesar_video
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
from utils.bot_state import BotState
from layers.mainLayer import register_message_and_process
from services.aiService import AIClass
from promuevo.services.aiService import AIClassPromuevo
from promuevo.layers.mainLayerPromuevo import register_message_and_process_promuevo
from twitter.executions.Reply import single_response_preview ,respond_to_tweet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


bot_state =BotState()
api_key =os.environ.get("OPEN_AI_KEY")
ai = AIClass(api_key=api_key, model="gpt-4o")
aiPromuevo = AIClassPromuevo(api_key=api_key, model="gpt-4o")

class BotAssignment(BaseModel):
    profileId: int
    botCount: int

class ReplyTweetData(BaseModel):
    tweetId: str
    indication: str
    hashtags: list[str]
    botAssignments: list[BotAssignment]

#Initiate App
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

#CORS - Origins
origins = ["*"]

#CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

load_dotenv()

url =os.environ.get("SUPABASE_URL")
key =os.environ.get("SUPABASE_KEY")
supabase=create_client(url,key)

#Check Health
@app.get("/health")
async def checkHealth():
    return {"message": "Healthy"}

# Post bot response

@app.post("/post-texto")
async def post_texto(data:dict):

    inicio = time.time()
    message_decoded = data["question"]
    id = data["id"]
    print(message_decoded)
    print("id identificado:",id)
    #aqui hacer la petición a la base de datos dependiendo del id que mande del usuario
    response = get_chat_response(message_decoded,id)
    print(response)
    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(f"total time: {int(tiempo_transcurrido // 60)} minutos y {int(tiempo_transcurrido % 60)} segundos")

    return {"response": response}

@app.post("/post-texto-audio")
async def post_texto_out_audio(data:dict):

    inicio = time.time()
    message_decoded = data["question"]
    id = data["id"]
    print(message_decoded)
    print("id identificado:",id)
    chat_response = get_chat_response(message_decoded,id)
        # Guardia: Asegurar salida
    if not chat_response:
        raise HTTPException(status_code=400, detail="Falló la respuesta del chat")
    print(chat_response)

    companyId = getCompanyId(id)
    voiceSource = getVoiceSource(companyId)
    if voiceSource == "openai":
        voice = getExactVoice(companyId)
        audio_output = speech_to_text_openai(input_text=chat_response,voice=voice)
    else:
        voice = getExactVoice(companyId)
        stability = getStability(companyId)
        similarity =getSimilarity(companyId)
        style = getStyle(companyId)
        audio_output = convert_text_to_speech_multilingual(chat_response,voice,stability,similarity,style)

    # Guardia: Asegurar salida
    if not audio_output:
        raise HTTPException(status_code=400, detail="Falló la salida de audio")

    print("audio convertido a wav")
    # Crear un generador que produce fragmentos de datos
    def iterfile():
        yield audio_output
    return StreamingResponse(iterfile(), media_type="application/octet-stream")


@app.post("/post-texto-audio-eleven")
async def post_texto_out_audio(data:dict):

    inicio = time.time()
    message_decoded = data["question"]
    id = data["id"]
    print(message_decoded)
    print("id identificado:",id)
    chat_response = get_chat_response(message_decoded,id)
        # Guardia: Asegurar salida
    if not chat_response:
        raise HTTPException(status_code=400, detail="Falló la respuesta del chat")
    print(chat_response)

    companyId = getCompanyId(id)
    voice = getExactVoice(companyId)
    stability = getStability(companyId)
    similarity =getSimilarity(companyId)
    style = getStyle(companyId)
    audio_response = convert_text_to_speech_multilingual(chat_response,voice,stability,similarity,style)

    print("audio convertido a WAV")
    def iterfile():
        yield audio_response

    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(f"total time: {int(tiempo_transcurrido // 60)} minutos y {int(tiempo_transcurrido % 60)} segundos")

    return StreamingResponse(iterfile(), media_type="application/octet-stream")

####endpoint beta 1.1

@app.post("/post_texto_audio_openai")
async def post_texto_out_audio(data:dict):

    inicio = time.time()
    message_decoded = data["question"]
    id = data["id"]
    print(message_decoded)
    print("id identificado:",id)
    chat_response = get_chat_response(message_input=message_decoded,id=id)
        # Guardia: Asegurar salida
    if not chat_response:
        raise HTTPException(status_code=400, detail="Falló la respuesta del chat")
    print(chat_response)

    companyId = getCompanyId(id)
    voice = getExactVoice(companyId)
    audio_response = speech_to_text_openai(input_text=chat_response,voice=voice)

    if not chat_response:
        raise HTTPException(status_code=400, detail="Falló la respuesta del audio")
    print("audio convertido a WAV")
    def iterfile():
        yield audio_response

    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(f"total time: {int(tiempo_transcurrido // 60)} minutos y {int(tiempo_transcurrido % 60)} segundos")

    return StreamingResponse(iterfile(), media_type="application/octet-stream")

@app.post("/post_audio_audio_openai")
async def post_audio(file: UploadFile = File(...), id: str = Form(...)):

    # Convert audio to text - production
    # Save the file temporarily
    inicio = time.time()
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
    audio_output = speech_to_text_openai(input_text=chat_response)

    # Guardia: Asegurar salida
    if not audio_output:
        raise HTTPException(status_code=400, detail="Falló la salida de audio")

    print("audio convertido a wav")
    # Crear un generador que produce fragmentos de datos
    def iterfile():
        yield audio_output
    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(f"total time: {int(tiempo_transcurrido // 60)} minutos y {int(tiempo_transcurrido % 60)} segundos")

    # Usar para Post: Devolver audio de salida
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

@app.post("/post-audio-eleven")
async def post_audio(file: UploadFile = File(...), id: str = Form(...)):

    # Convert audio to text - production
    # Save the file temporarily
    inicio = time.time()
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


    companyId = getCompanyId(id)
    voice = getExactVoice(companyId)
    stability = getStability(companyId)
    similarity =getSimilarity(companyId)
    style = getStyle(companyId)
    audio_output = convert_text_to_speech_multilingual(chat_response,voice,stability,similarity,style)

    # Guardia: Asegurar salida
    if not audio_output:
        raise HTTPException(status_code=400, detail="Falló la salida de audio")

    print("audio convertido a wav")
    # Crear un generador que produce fragmentos de datos
    def iterfile():
        yield audio_output
    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(f"total time: {int(tiempo_transcurrido // 60)} minutos y {int(tiempo_transcurrido % 60)} segundos")

    # Usar para Post: Devolver audio de salida
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

@app.post("/post-audio")
async def post_audio_new(file: UploadFile = File(...),  id: str = Form(...)):

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

    companyId = getCompanyId(id)
    voiceSource = getVoiceSource(companyId)
    if voiceSource == "openai":
        voice = getExactVoice(companyId)
        audio_output = speech_to_text_openai(input_text=chat_response,voice=voice)
    else:
        voice = getExactVoice(companyId)
        stability = getStability(companyId)
        similarity =getSimilarity(companyId)
        style = getStyle(companyId)
        audio_output = convert_text_to_speech_multilingual(chat_response,voice,stability,similarity,style)

    # Guardia: Asegurar salida
    if not audio_output:
        raise HTTPException(status_code=400, detail="Falló la salida de audio")

    print("audio convertido a wav")
    # Crear un generador que produce fragmentos de datos
    def iterfile():
        yield audio_output
    return StreamingResponse(iterfile(), media_type="application/octet-stream")


@app.post("/signup")
async def signup(data: dict):
    email = data.get("email")
    id_company = data.get("id_company")
    
    if not email or not id_company:
        raise HTTPException(status_code=400, detail="Email or company ID missing.")

    try:
        response = supabase.auth.sign_up(data)
    except AuthApiError as error:
        print("Error during registration:", str(error))
        raise HTTPException(status_code=400, detail=str(error))


    try:
        supabase.table("Users").insert({"Email": email, "id_company": id_company}).execute()
    except Exception as e:
        print("Error inserting user:", str(e))
        raise HTTPException(status_code=500, detail="Failed to insert user into database.")
    
    return response

@app.post("/login")
async def login(data:dict):
    session = supabase.auth.sign_in_with_password(data)
    print(session)
    access_token = session.session.access_token
    print(access_token)
    return access_token


@app.post("/login_empresas")
async def login(data: dict):
    try:
        # Intenta iniciar sesión con Supabase
        session = supabase.auth.sign_in_with_password(data)
        # Recupera el token de acceso desde la respuesta
        access_token = session.session.access_token
        print(access_token)
        # Retorna el token de acceso y el estado de autenticación
        return JSONResponse(content={'isAuthenticated': True, 'token': access_token})

    except Exception as e:
        # Imprime el error y retorna una respuesta con el estado de error
        print("Razón del error:", str(e))
        return JSONResponse(status_code=400, content={'isAuthenticated': False, 'error': str(e)})

@app.post("/forgot-password")
async def forgot_password(data:dict):
    email=data["email"]
    options = {
    'redirect_to': 'https://branimax-analisis-front.vercel.app/change-password'}
    response = supabase.auth.reset_password_email(email,options=options)
    print(response)
    return

@app.post("/logout")
async def forgot_password():
    supabase.auth.sign_out()
    print("sesion finalizada")
    return

@app.post("/get-company")
async def get_company():
    data = supabase.table("Companys").select("*").execute()
    print(data)
    return data

@app.post("/get-resume")
async def generate_resume(data:dict):
    company_name = data["company_name"]
    topics = found_topics(company_name)
    print(topics)
    return {"response": topics}

@app.post("/ask_question")
async def generate_ask(data:dict):
    company_name = data["company_name"]
    question = data["question"]
    response = generate_question(company_name,question)
    print(response)
    return {"response": response}

@app.post("/sign-out")
async def sign_out():
    supabase.auth.sign_out()
    print("sign out")

from typing import Optional

@app.post("/change-password")
async def change_password(data: dict):
    password = data["password"]
    access_token = data["access_token"]
    refresh_token =data["refresh_token"]

    attributes = {
        "password": password
    }
    
    try:
        data = supabase.auth.set_session(access_token,refresh_token)
        response = supabase.auth.update_user(attributes)
        print(response)
        
        if response.error:
            print("Error:", response.error)
            return {"error": str(response.error)}
        
        return response.data  # o simplemente `return response`
    except Exception as e:
        print(f"Error general: {str(e)}")
        return {"error": f"Error general: {str(e)}"}

@app.post("/sign-up-empresas")
async def signup(data: dict):
    email = data.get("email")
    
    id_company = data.get("id_company")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email or company ID missing.")

    try:
        response = supabase.auth.sign_up(data)
    except AuthApiError as error:
        print("Error during registration:", str(error))
        raise HTTPException(status_code=400, detail=str(error))


    try:
        supabase.table("Users").insert({"Email": email, "id_company": id_company}).execute()
    except Exception as e:
        print("Error inserting user:", str(e))
        raise HTTPException(status_code=500, detail="Failed to insert user into database.")
    
    return response

@app.post("/get-users-resume")
async def get_users_resume(data:dict):
    company_name = data["company_name"]
    total_users = get_resume_users(company_name)
    return {"response": total_users}


@app.post("/get-users-info")
async def user_info(data:dict):
    company_name = data["company_name"]
    users = get_info_users(company_name)
    return {"response": users}


@app.post("/get-users-conversation")
async def user_conversation(data:dict):
    id = data["id_user"]
    print(id)
    conversation = conversation_by_user(id_user=id)
    return {"response": conversation}


@app.post("/whatsapp")
async def message(request: Request):
    form_data = await request.form()
    id=18

    if "MediaContentType0" in form_data:
        media_url = form_data["MediaUrl0"]
        response = requests.get(media_url)
        audio_data = response.content

        if response.status_code == 200:

            audio_oga_path = os.path.join(STATIC_DIR,"audio.oga")
            with open(audio_oga_path, "wb") as file:
                file.write(audio_data)
            print("archivo de audio descargado")

            audio = AudioSegment.from_file(audio_oga_path, format="ogg")
            audio_wav_path = os.path.join(STATIC_DIR, "audio.wav")
            audio.export(audio_wav_path, format="wav")

            with open(audio_wav_path, "rb") as audio_file:
                message_decoded = convert_audio_to_text(audio_file)
            #Hardcoded ID at the moment
            chat_response = get_chat_response(message_decoded,id)
            print(chat_response)

            audio_output = convert_text_to_speech_whatsapp(chat_response)
            print("audio generado")

            if not audio_output:
                raise HTTPException(status_code=400, detail="Falló la salida de audio")
            
            audio_output_path = os.path.join(STATIC_DIR, "audio_response.mp3")
            with open(audio_output_path, "wb") as audio_file:
                audio_file.write(audio_output)

            response = MessagingResponse()
            message = Message()
            message.body(chat_response)
            message.media('https://servidorscarlett.com/static/audio_response.mp3')
            response.append(message)

            return Response(content=str(response), media_type="application/xml")
        
        else:
            return {"error": "Failed to download media"}
    
    else:
        incoming_que = (await request.form()).get('Body', '').lower()
        print(incoming_que)

        chat_response = get_chat_response(incoming_que,id) #hardcoded at the moment
        print(chat_response)
        bot_resp =MessagingResponse()
        msg = bot_resp.message()
        msg.body(chat_response)

        return Response(content=str(bot_resp), media_type="application/xml")
    

@app.post("/generate_resume")
async def generate_resume(data:dict):
    text = data["text"]
    response = getResumeNote(text)
    return {"response": response}

@app.post("/tavus_endpoint")
async def serve_avatar(data:dict):
    script = data["script"]
    title = data["title"]
    download_url, stream_url = procesar_video(script =script,video_name= title)
    return {"download_url": download_url, "stream_url": stream_url}

@app.post("/whatsapp_calendar")
async def message(request: Request):
    form_data = await request.form()
    incoming_que = form_data.get('Body', '').lower()
    from_number = form_data.get('From')
    print(f"Mensaje recibido de {from_number}: {incoming_que}")
    
    bot_response = MessagingResponse()
    message = bot_response.message()
    
    if incoming_que == "borrar":
        delete_state(from_number)
        message.body("registro borrado")
        return Response(content=str(bot_response), media_type="application/xml")
    
    chat_response = await register_message_and_process(incoming_que, bot_state, ai, from_number)
    message.body(chat_response)
    return Response(content=str(bot_response), media_type="application/xml")

@app.post("/whatsapp_alcazar")
async def message(request: Request):
    form_data = await request.form()
    id=17
    bot_resp = MessagingResponse()
    msg = bot_resp.message()

    if "MediaContentType0" in form_data:
        media_url = form_data["MediaUrl0"]
        response = requests.get(media_url)
        audio_data = response.content

        if response.status_code == 200:
            audio_oga_path = os.path.join(STATIC_DIR,"audio.oga")
            with open(audio_oga_path,"wb") as file:
                file.write(audio_data)
            print("Archivo de audio descargado")

            audio = AudioSegment.from_file(audio_oga_path, format="ogg")
            audio_wav_path = os.path.join(STATIC_DIR,"audio.wav")
            audio.export(audio_wav_path,format="wav")

            with open(audio_wav_path,"rb") as audio_file:
                message_decoded = convert_audio_to_text(audio_file)
            chat_response = get_chat_response(message_decoded,id)
            print(chat_response)
        else: 
            chat_response= "error al descargar el archivo de audio"

    else:        
        incoming_que = (await request.form()).get('Body', '').lower()
        print(incoming_que)
        chat_response = get_chat_response(incoming_que,id)
        print(chat_response)
    
    msg.body(chat_response)
    return Response(content=str(bot_resp), media_type="application/xml")

@app.post("/promuevo")
async def message(data:dict):
    incoming_que= data["question"]
    id = data["id"]
    user_id =data["user_id"]
    database = "promuevodb"
    print(incoming_que)

    if incoming_que == "reiniciar":
        delete_state(database,user_id)
        response = "proceso Reiniciado"
        return {"response": response}
    
    response = await register_message_and_process_promuevo(incoming_que,bot_state,aiPromuevo,user_id,database)
    
    return {"response": response}

@app.post("/simulate_tweet")
async def simulate_tweet(data: dict):
    tweetId = data.get("tweetId")
    hashtags = data.get("hashtags", [])
    indication = data.get("indication")
    profile_id = data.get("profile", {}).get("id")
    response = single_response_preview(tweetId,profile_id,indication,hashtags)
    return response

@app.post("/respond_to_tweet")
async def reply_tweet(data: ReplyTweetData):
    try:
        print(data)
        respond_to_tweet(data.tweetId, data.indication, data.hashtags, data.botAssignments)
        return {"response": "Tweet responded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


