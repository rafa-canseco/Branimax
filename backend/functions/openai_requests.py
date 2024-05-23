# from openai import OpenAI
from decouple import config
from langchain_community.callbacks import get_openai_callback
from langchain_community.document_loaders import CSVLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.messages import HumanMessage, SystemMessage
from functions.querys_db import getPromtByCompany,getConversationSaved,getUrlCsvForContext,getCompanyId
import os
import re
from langchain_openai import ChatOpenAI
from openai import OpenAI


#retrieve our eviroment variables
os.environ["OPENAI_API_KEY"] =config("OPEN_AI_KEY")
OpenAI.api_key = config("OPEN_AI_KEY")
client = OpenAI()


def clean_response_text(text):
    cleaned_text = (text.encode().decode('unicode_escape'))
    cleaned_text = re.sub(r'\s+',' ',cleaned_text)
    return cleaned_text

def fix_encoding(text):
    try:
        corrected_text = text.encode('iso-8859-1').decode('utf-8')
        return corrected_text
    except Exception as e:
        print(f"Error fixing encoding: {e}")
        return text  # Devuelve el texto original si hay un error

#convert audio to text
def convert_audio_to_text(audio_file):
    try:

        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
        transcription = response.text
        print(transcription)
        return transcription
    except Exception as e:
        print(e)
        return

    #test
def get_chat_response(message_input,id):

    try:
        #aqui relacionamos el prompt al usuario 
        print(id)
        csv = getUrlCsvForContext(id)

        with get_openai_callback() as cb:
            # Cargar el documento con los datos del cliente

            loader = PyPDFLoader(csv)
            documents = loader.load()

            # Dividir el documento en fragmentos
            text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap=0)
            texts = text_splitter.split_documents(documents)
            # Crear los embeddings
            embeddings = OpenAIEmbeddings()
            # Crear el índice de vectores
            db = Chroma.from_documents(texts,embeddings)
            retriever = db.as_retriever(search_type="similarity",search_kwargs={"k":2})
            # Iniciar el modelo de lenguaje, definir la temperatura y el modelo
            llm = ChatOpenAI(model='gpt-4o')
            # Definir la plantilla del mensaje 
            id_company = getCompanyId(id)
            template = getPromtByCompany(id_company)
            # Incluir el nuevo prompt
            custom_prompt = PromptTemplate(template=template,input_variables=["context","question"])
            # Crear una instancia de RetrievalQA con el modelo de lenguaje, el tipo de cadena y el recuperador
            qa = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=retriever,return_source_documents=False,chain_type_kwargs={"prompt":custom_prompt})
            response = qa.invoke({"query":message_input})
            print(response['result'])

            # getConversationSaved(id,message_input=message_input,response=response)

            # Imprimir las estadísticas de la solicitud
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Successful Requests: {cb.successful_requests}")
            print(f"Total Cost (USD): ${cb.total_cost}")
            # Devolver el texto del mensaje
            return response['result']
    except Exception as e:
        print(e)
        return

def getResumeNote(text):

    # prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI(model='gpt-4o')
    llm_chain =  llm
    instruction = f"Sintetiza la siguiente nota periodística con máximo 100 palabras: {text}"
    messages = [HumanMessage(content=instruction)]
    response = llm.invoke(messages)
    print(response.content)
    return response.content 


text = """
### Avances en Git: Soluciones a Problemas de Conectividad

En el ámbito del desarrollo de software, Git sigue siendo la herramienta de referencia para la gestión de versiones. No obstante, recientes reportes de desarrolladores han destacado problemas de conectividad al ejecutar comandos como `git pull`, con errores relacionados a la comunicación HTTP/2.

Estos incidentes, aunque esporádicos, resaltan la necesidad de una conexión a Internet robusta y la importancia de mantener las herramientas actualizadas. Entre las soluciones propuestas se incluyen reintentar la operación, ajustar configuraciones de buffer HTTP, y forzar el uso de HTTP/1.1 en lugar de HTTP/2.

La comunidad de desarrolladores se mantiene atenta y proactiva, buscando constantemente mejorar la experiencia del usuario. Estos esfuerzos aseguran que Git continúe siendo una herramienta confiable y eficiente para la colaboración y el control de versiones en proyectos de software.
"""

getResumeNote(text)