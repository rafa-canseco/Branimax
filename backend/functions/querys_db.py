from supabase import create_client
from dotenv import load_dotenv
import os
import requests
load_dotenv()
import json

url =os.environ.get("SUPABASE_URL")
key =os.environ.get("SUPABASE_KEY")
supabase=create_client(url,key)

def download_csv_from_url(url, folder_path, file_name):
    response = requests.get(url)
    with open(os.path.join(folder_path, file_name), 'w') as file:
        file.write(response.text)

def getUrlCsvForContext(id):
    companyName = getCompanyName(id)
    # Descargar el archivo CSV y guardarlo en la carpeta deseada
    folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'storage'))
    file_name = f"{companyName}.csv"
    full_file_path = os.path.join(folder_path, file_name)
    # Crear el directorio si no existe
    os.makedirs(folder_path, exist_ok=True)
    # Verificar si el archivo ya existe
    if not os.path.exists(full_file_path):
        csv_supabase = supabase.table("Particularities").select("context").eq("id_company", id).execute()
        if not csv_supabase.data:
            raise ValueError("Id:Error Company not registered")
        csv_url = csv_supabase.data[0]['context']
        print(csv_url)
        download_csv_from_url(csv_url, folder_path, file_name)
    return full_file_path

def getPromtByCompany(id):
    template_supabase = supabase.table("Particularities").select("prompt").eq("id_company", id).execute()
    if not template_supabase.data:
        raise ValueError("Id:Error Company not registered")
    template = template_supabase.data[0]['prompt']
    return template

def getCompanyName(id):
    companyName = supabase.table("Companys").select("name").eq("id", id).execute().data[0]['name']
    return companyName

def getConversationSaved(id, message_input, response):
    current_record = supabase.table("Conversation").select("text").eq("id_user", id).execute()
    # Si no hay una conversación existente, iniciamos una en la base de datos
    if not current_record.data:
        # Creamos el texto actualizado con el mensaje del usuario y la respuesta de Scarlett
        updated_text = "\nUsuario: " + message_input + "\nScarlett: " + response
        new_conversation = supabase.table("Conversation").insert({"text": updated_text, "id_user": id}).execute()
        print("Nueva conversación iniciada:", new_conversation)
    else:
        existing_text = current_record.data[0]['text'] if current_record.data[0]['text'] is not None else ""
        # Actualizamos el texto con el mensaje del usuario y la respuesta de Scarlett
        updated_text = existing_text + "\nUsuario: " + message_input + "\nScarlett: " + response
        # Actualizamos el registro en la base de datos con el nuevo texto
        update_response = supabase.table("Conversation").update({"text": updated_text}).eq("id_user", id).execute()
    # Verificamos que el registro se haya actualizado correctamente
    verification_record = supabase.table("Conversation").select("text").eq("id_user", id).execute()

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

def getCompanyConversation(company_name):
    company_id = supabase.table("Companys").select("id").eq("name", company_name).execute().data[0]['id']
    users = supabase.table("Users").select("id").eq("id_company", company_id).execute()
    users_id = [user['id'] for user in users.data]
    
    conversations_data = []
    conversation_counter = 0
    
    for uid in users_id:
        conversations = supabase.table("Conversation").select("text").eq("id_user", uid).execute()
        for conversation in conversations.data:
            conversation_counter += 1
            conversations_data.append({
                "user_id": uid,
                "conversation_number": conversation_counter,
                "text": conversation['text']
            })
    
    json_output = json.dumps({"conversations": conversations_data}, indent=4)
    print("conversaciones terminadas correctamente")
    
    return json_output


def get_total_users(company_name):
    company_id = supabase.table("Companys").select("id").eq("name", company_name).execute().data[0]['id']
    users = supabase.table("Users").select("id").eq("id_company", company_id).execute()
    print(users)
    total_users = len(users.data)
    print(total_users)
    return total_users

def get_info_users_global(company_name):
    company_name = supabase.table("Companys").select("id").eq("name", company_name).execute().data[0]['id']
    users = supabase.table("Users").select("*").eq("id_company", company_name).execute()
    print(users)
    return users

def conversation_by_user(id_user):
    conversation =supabase.table("Conversation").select("text").eq("id_user", id_user).execute().data[0]['text']
    print(conversation)
    return conversation



