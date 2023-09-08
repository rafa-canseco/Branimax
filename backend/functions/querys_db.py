from supabase import create_client
from dotenv import load_dotenv
import os
import requests
load_dotenv()

url =os.environ.get("SUPABASE_URL")
key =os.environ.get("SUPABASE_KEY")
supabase=create_client(url,key)

def download_csv_from_url(url, folder_path, file_name):
    response = requests.get(url)
    with open(os.path.join(folder_path, file_name), 'w') as file:
        file.write(response.text)

def getUrlCsvForContext(id):
    csv_supabase = supabase.table("Particularities").select("context").eq("id_company", id).execute()
    if not csv_supabase.data:
        raise ValueError("Id:Error Company not registered")
    csv_url = csv_supabase.data[0]['context']
    print(csv_url)
    companyName = supabase.table("Companys").select("name").eq("id", id).execute().data[0]['name']
    # Descargar el archivo CSV y guardarlo en la carpeta deseada
    folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'storage'))
    file_name = f"{companyName}.csv"
    full_file_path = os.path.join(folder_path, file_name)
    # Crear el directorio si no existe
    os.makedirs(folder_path, exist_ok=True)
    # Verificar si el archivo ya existe
    if not os.path.exists(full_file_path):
        download_csv_from_url(csv_url, folder_path, file_name)
    return full_file_path

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