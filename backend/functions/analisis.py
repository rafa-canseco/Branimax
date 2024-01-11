from supabase import create_client
from dotenv import load_dotenv
import os
import requests
from functions.querys_db import getCompanyConversation,get_total_users,get_info_users_global
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import create_extraction_chain
from langchain.callbacks import get_openai_callback
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import SupabaseVectorStore,Chroma
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain import OpenAI
import openai
import time
import os
from dotenv import load_dotenv
from decouple import config
import time
load_dotenv()

url =os.environ.get("SUPABASE_URL")
key =os.environ.get("SUPABASE_KEY")
supabase=create_client(url,key)
os.environ["OPENAI_API_KEY"] =config("OPEN_AI_KEY")
openai.api_key = config("OPEN_AI_KEY")

llm3= ChatOpenAI(temperature=0,
                         openai_api_key= os.getenv("OPEN_AI_KEY"),
                         model_name="gpt-3.5-turbo",
                         request_timeout=220
                         )

def generate_docs(conversaciones):
    with get_openai_callback() as cb:
        inicio = time.time()
        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " "], chunk_size=10000, chunk_overlap=2200)
        metadatas = [{"some_key": "some_value"}]  # Asegúrate de generar metadatas significativos

        docs = text_splitter.create_documents([conversaciones],metadatas)
        print("documentos terminados correctamente")
        print (f"You have {len(docs)} docs. First doc is {llm3.get_num_tokens(docs[0].page_content)} tokens")
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        fin = time.time()
        tiempo_transcurrido = fin - inicio
        print(f"generate docs lasted: {int(tiempo_transcurrido // 60)} minutos y {int(tiempo_transcurrido % 60)} segundos")
        return docs
    
def split_docs(conversaciones):
    with get_openai_callback() as cb:
        inicio = time.time()
        print("inicio")
        text_splitter = RecursiveCharacterTextSplitter( chunk_size=2000, chunk_overlap=0)
        docs = text_splitter.split_text(conversaciones)
        print("documentos terminados correctamente")
        print (f"You have {len(docs)} docs. First doc is tokens")
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        fin = time.time()
        tiempo_transcurrido = fin - inicio
        print(f"generate docs lasted: {int(tiempo_transcurrido // 60)} minutos y {int(tiempo_transcurrido % 60)} segundos")
        return docs

def found_topics(company_name):
    with get_openai_callback() as cb:

        llm4=ChatOpenAI(temperature=0,
                            openai_api_key= os.getenv("OPEN_AI_KEY"),
                            model_name="gpt-4",
                            request_timeout=220
                            )
        inicio = time.time()
        conversaciones_json = getCompanyConversation(company_name)
        docs = generate_docs(conversaciones_json)
        template = """
        Eres un asistente que analiza conversaciones para una empresa de marketing. 
        Las conversaciones son entre usuarios humanos (denominados "Usuario") y una inteligencia artificial llamada "Scarlett". Cada "user_id" corresponde a un usuario distinto, y "conversation_number" señala el número de la conversación. El "text" se refiere al contenido textual de la conversación.
        Recibirás un JSON con varias conversaciones y tu tarea es extraer insights valiosos. A continuación, identifica los temas discutidos y proporciona un enunciado breve que describa cada tema.
        Instrucciones:
        - Después del nombre del tema, proporciona una breve descripción. Ejemplo: 'Topic: Brief Description'.
        - Solo responde con puntos relevantes a la conversación. Si no identificas temas, indica 'No Topics'.
        - Utiliza viñetas para enumerar los temas, no números.
        - Extrae temas solo del transcript proporcionado, evita usar ejemplos.
        - Los títulos de los temas deben ser descriptivos pero concisos. Ejemplo: 'Shaan's Interesting Projects At Twitch' en lugar de 'Shaan's Experience at Twitch'.
        - Un tema debe ser sustancial, no un comentario aislado.
        - Entrega tu respuesta final en español.
        EJEMPLO DE LA CONVERSACIÓN A RECIBIR:
        Recibirás un JSON con el siguiente formato:
        "user_id": 1,
        "conversation_number": 1,
        "text": "Usuario: -user input- Scarlett: -AI input-"
        EJEMPLO DE RESPUESTA A DAR:
        - Sam’s Elisabeth Murdoch Story: Sam recibió una llamada de Elisabeth Murdoch cuando lanzó The Hustle. Ella quería producir contenido en video.
        - Shaan’s Rupert Murdoch Story: Shaan fue invitado a un evento de Rupert Murdoch en Las Vegas cuando dirigía Blab.
        - Revenge Against The Spam Calls: Empresas como RoboCall, TrueCaller, DoNotPay y FitIt protegen a los consumidores de llamadas spam.
        - Collecting: Shaan propuso crear un mercado móvil para coleccionistas, similar a lo que hace StockX con zapatillas premium.
        """
        system_message_prompt_map = SystemMessagePromptTemplate.from_template(template)

        human_template="Transcript: {text}" # Simply just pass the text as a human message
        human_message_prompt_map = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt_map = ChatPromptTemplate.from_messages(messages=[system_message_prompt_map, human_message_prompt_map])


        template ="""
        Eres un asistente que analiza conversaciones para una empresa de marketing. 
        - Se te proporcionará una serie de temas en formato de lista.
        - Tu objetivo es extraer los nombres de los temas y proporcionar una descripción breve de una sola oración para cada tema.
        - Elimina cualquier punto duplicado que veas.
        - Extrae los temas únicamente del transcript proporcionado. No uses los ejemplos como referencia.
        - Entrega tu respuesta final en español.

        % INICIO DE LOS EJEMPLOS
        - Historia de Sam con Elisabeth Murdoch: Sam recibió una llamada de Elisabeth Murdoch justo después de lanzar "The Hustle", ya que ella quería producir contenido en video.
        - Historia de Shaan con Rupert Murdoch: Cuando Shaan dirigía "Blab", fue invitado a un evento organizado por Rupert Murdoch durante el CES en Las Vegas.
        % FIN DE LOS EJEMPLOS
        """
        system_message_prompt_map = SystemMessagePromptTemplate.from_template(template)

        human_template="Transcript: {text}" # Simply just pass the text as a human message
        human_message_prompt_map = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt_combine = ChatPromptTemplate.from_messages(messages=[system_message_prompt_map, human_message_prompt_map])

        chain = load_summarize_chain(llm4,
                                    chain_type="map_reduce",
                                    map_prompt=chat_prompt_map,
                                    combine_prompt=chat_prompt_combine,
                                    verbose=False
                                    )
        print("iniciando cadena")
        topics_found = chain.run({"input_documents":docs})
        print("----------")
        print("Topics found:")
        print(topics_found)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        fin=time.time()
        tiempo_transcurrido = fin - inicio
        print(f"found topics lasted: {int(tiempo_transcurrido // 60)} minutos y {int(tiempo_transcurrido % 60)} segundos")
        return topics_found

def scheme_topics(topics):
    with get_openai_callback() as cb:
        inicio =time.time()
        schema = {
        "properties": {
            # The title of the topic
            "topic_name": {
                "type": "string",
                "description" : "The title of the topic listed"
            },
            # The description
            "description": {
                "type": "string",
                "description" : "The description of the topic listed"
            },
            "tag": {
                "type": "string",
                "description" : "The type of content being described",
                "enum" : ['Business Models', 'Life Advice', 'Health & Wellness', 'Stories']
            }
        },
        "required": ["topic", "description"],
        }
        chain = create_extraction_chain(schema,llm3)
        topics_structured = chain.run(topics)
        print("---------------------------")
        print(topics_structured)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        fin= time.time()
        tiempo_transcurrido = fin - inicio
        print(f"found schema lasted: {int(tiempo_transcurrido // 60)} minutos y {int(tiempo_transcurrido % 60)} segundos")


def generate_question(company_name,question):
    with get_openai_callback() as cb:
        inicio = time.time()
        conversation = getCompanyConversation(company_name)
        docs = split_docs(conversation)
        embeddings = OpenAIEmbeddings()
        db=Chroma.from_texts(docs,embeddings)
        retriever = db.as_retriever(search_type="similarity",search_kwargs={"k":1})
        qa = RetrievalQA.from_chain_type(llm = OpenAI(model='gpt-3.5_turbo-instruct'),chain_type="stuff",retriever=retriever,return_source_documents=True)
        query = question
        result= qa({"query":query})
        print(result)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        fin = time.time()
        tiempo_transcurrido = fin - inicio
        print(f"question resolved lasted: {int(tiempo_transcurrido // 60)} minutos y {int(tiempo_transcurrido % 60)} segundos")
        return result

def get_resume_users(company_name):
    total_usuarios = get_total_users(company_name)
    return total_usuarios

def get_info_users(company_name):
    users = get_info_users_global(company_name)
    return users

