from supabase import create_client
from dotenv import load_dotenv
import os
load_dotenv()

url =os.environ.get("SUPABASE_URL")
key =os.environ.get("SUPABASE_KEY")
supabase=create_client(url,key)

def getPromtByCompany(id):
    template_supabase = supabase.table("Particularities").select("prompt").eq("id_company", id).execute()
    if not template_supabase.data:
        raise ValueError("Id:Error Company not registered")
    template = template_supabase.data[0]['prompt']
    print(template)
    return template

def getConversationSaved(id,message_input,response):
    current_record = supabase.table("Conversation").select("text").eq("id", id).execute()
    existing_text = current_record.data[0]['text'] if current_record.data[0]['text'] is not None else ""
    print("Texto existente:", existing_text)   
    # Actualizamos el texto con el mensaje del usuario y la respuesta de Scarlett
    updated_text = existing_text + "\nUsuario: " + message_input + "\nScarlett: " + response
    print("Texto actualizado:", updated_text)   
    # Actualizamos el registro en la base de datos con el nuevo texto
    update_response = supabase.table("Conversation").update({"text": updated_text}).eq("id", id).execute()
    print(update_response)
    # Verificamos que el registro se haya actualizado correctamente
    verification_record = supabase.table("Conversation").select("text").eq("id", id).execute()
    print("Registro de verificación:", verification_record)

def getVoice(id):
    voz_supabase = supabase.table("Particularities").select("voice").eq("id_company", id).execute()
    voz = voz_supabase.data[0]['voice']
    print(voz)
    return voz

def getStability(id):
    stability_supabase = supabase.table("Particularities").select("voice_stability").eq("id_company", id).execute()
    stability = stability_supabase.data[0]['voice_stability']
    print(stability)
    return stability

def getSimilarity(id):
    similarity_supabase = supabase.table("Particularities").select("voice_similarity").eq("id_company", id).execute()
    similarity = similarity_supabase.data[0]['voice_similarity']
    print(similarity)
    return similarity

def getStyle(id):
    style_supabase = supabase.table("Particularities").select("voice_style").eq("id_company", id).execute()
    style = style_supabase.data[0]['voice_style']
    print(style)
    return style