#uvicorn main:app

#Main Imports
from fastapi import FastAPI,File,UploadFile,HTTPException,Form
from fastapi.responses import StreamingResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from gotrue.errors import AuthApiError
import os
from supabase import create_client
import time


from dotenv import load_dotenv

#Custom Function Imports
from functions.openai_requests import convert_audio_to_text,get_chat_response
from functions.text_to_speech import convert_text_to_speech
from functions.analisis import found_topics,scheme_topics,generate_question,get_resume_users,get_info_users
from functions.querys_db import conversation_by_user

#Initiate App
app = FastAPI()

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


@app.post("/post-audio")
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
    
    # Convertir rßespuesta del chat a audio
    audio_output = convert_text_to_speech(chat_response,id)

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
