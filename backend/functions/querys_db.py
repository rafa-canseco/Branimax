from supabase import create_client
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
import os
import requests
from decouple import config
load_dotenv()
import json
from datetime import datetime
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

url =os.environ.get("SUPABASE_URL")
key =os.environ.get("SUPABASE_KEY")
supabase=create_client(url,key)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()

def download_csv_from_url(url, folder_path, file_name):
    response = requests.get(url)
    response.raise_for_status()
    with open(os.path.join(folder_path, file_name), 'wb') as file:
        file.write(response.content)

def getUrlCsvForContext(id):
    companyName = getCompanyName(id)
    company_id = getCompanyId(id)
    # Descargar el archivo CSV y guardarlo en la carpeta deseada
    folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'storage'))
    file_name = f"{companyName}.pdf"
    full_file_path = os.path.join(folder_path, file_name)
    # Crear el directorio si no existe
    os.makedirs(folder_path, exist_ok=True)
    # Verificar si el archivo ya existe
    if not os.path.exists(full_file_path):
        csv_supabase = supabase.table("Particularities").select("context").eq("id_company", company_id).execute()
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
    company_id = getCompanyId(id)
    companyName = supabase.table("Companys").select("name").eq("id", company_id).execute().data[0]['name']
    print(companyName)
    return companyName

def getCompanyId(id):
    company_id= supabase.table("Users").select("id_company").eq("id",id).execute().data[0]['id_company']
    return company_id

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

def getVoiceSource(id_company):
    voice_Source = supabase.table("Particularities").select("voice_source").eq("id_company",id_company).execute()
    voiceSource = voice_Source.data[0]['voice_source']
    print(voiceSource)
    return voiceSource

def getExactVoice(id_company):
    exact_voice = supabase.table("Particularities").select("voice").eq("id_company",id_company).execute()
    exactVoice = exact_voice.data[0]['voice']
    print(exactVoice)
    return exactVoice

def datetime_to_str(state):
    for key, value in state.items():
        if isinstance(value, datetime):
            state[key] = value.isoformat()
    return state

def str_to_datetime(state):
    for key, value in state.items():
        try:
            state[key] = datetime.fromisoformat(value)
        except (ValueError, TypeError):
            pass
    return state


def get_state(from_number,database):
    response = supabase.table(database).select('*').eq('from_number', from_number).execute()
    if response.data:
        state_dict = json.loads(response.data[0]['state'])
        history = json.loads(response.data[0]['history'])
        history_persistent = response.data[0].get('history_persistent', [])
        state_dict = str_to_datetime(state_dict)
        return state_dict, history, history_persistent
    else:
        # Si el número no existe, crearlo
        supabase.table(database).insert({'from_number': from_number, 'state': '{}', 'history': '[]', 'history_persistent': '[]'}).execute()
        return {}, [], []
    
def get_talk_prompt(id):
    template_supabase = supabase.table("prompts_advanced_bot").select("prompt_hablar").eq("id_company",id).execute()
    if not template_supabase.data:
        raise ValueError("Prompt not setted")
    template = template_supabase.data[0]['prompt_hablar']
    print(template)
    return template

def get_discriminator_prompt(id):
    template_supabase = supabase.table("prompts_advanced_bot").select("discriminator_prompt").eq("id_company",id).execute()
    if not template_supabase.data:
        raise ValueError("Prompt not setted")
    template = template_supabase.data[0]['discriminator_prompt']
    return template

def get_calendar_prompt(id):
    template_supabase = supabase.table("prompts_advanced_bot").select("prompt_calendar").eq("id_company",id).execute()
    if not template_supabase.data:
        raise ValueError("Prompt not setted")
    template = template_supabase.data[0]['prompt_calendar']
    return template


def update_state(from_number, state, history, history_persistent,database):
    state = datetime_to_str(state)
    state_data = json.dumps(state)
    history_data = json.dumps(history)
    history_persistent_data = json.dumps(history_persistent)
    
    # Intentar actualizar el registro
    response, count = supabase.table(database).update({
        'state': state_data,
        'history': history_data,
        'history_persistent': history_persistent_data
    }).eq('from_number', from_number).execute()
    
    # Si no se actualizó ninguna fila, insertar el registro
    if count == 0:
        # Verificar si la columna 'from_number' existe
        columns = supabase.table(database).select('from_number').limit(1).execute()
        if 'from_number' not in columns.data[0]:
            # Crear la columna 'from_number' si no existe
            supabase.table(database).alter().add_column('from_number', 'text').execute()
        
        response, count = supabase.table(database).upsert({
            'from_number': from_number,
            'state': state_data,
            'history': history_data,
            'history_persistent': history_persistent_data
        }).execute()

def delete_state(database,fromUUID):
    supabase.table(database).delete().eq('from_number', fromUUID).execute()



def getPrompt(id):
    template_supabase = supabase.table("prompts").select("prompt").eq('id_name', id).execute()
    if not template_supabase.data:
        raise ValueError("Prompt not setted")
    template = template_supabase.data[0]['prompt']
    return template

def retrieveContext():
        vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase,
        table_name="documents",
        query_name="match_documents",
        )
        return vector_store

