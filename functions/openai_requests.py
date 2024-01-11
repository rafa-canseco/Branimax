from openai import OpenAI
from decouple import config
from langchain.callbacks import get_openai_callback
from langchain.document_loaders import CSVLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from functions.querys_db import getPromtByCompany,getConversationSaved,getUrlCsvForContext,getCompanyId
import os
import re
# test

print("error")
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

        transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
        )
        transcript_dict = vars(transcript)
        message_text = transcript_dict["text"]
        print(message_text)
        return message_text
    except Exception as e:
        print(e)
        return

    #test
def get_chat_response(message_input,id):
    from langchain.llms import OpenAI

    try:
        #aqui relacionamos el prompt al usuario 
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
            llm = OpenAI(model='gpt-3.5-turbo-instruct')
            # Definir la plantilla del mensaje 
            id_company = getCompanyId(id)
            template = getPromtByCompany(id_company)
            # Incluir el nuevo prompt
            custom_prompt = PromptTemplate(template=template,input_variables=["context","question"])
            # Crear una instancia de RetrievalQA con el modelo de lenguaje, el tipo de cadena y el recuperador
            qa = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=retriever,return_source_documents=False,chain_type_kwargs={"prompt":custom_prompt})
            # Ejecutar el modelo con el mensaje de entrada
            response = qa.run(message_input)
            cleaned_response =clean_response_text(response)
            corrected_response = fix_encoding(cleaned_response)
            getConversationSaved(id,message_input=message_input,response=corrected_response)

            # Imprimir las estadísticas de la solicitud
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Successful Requests: {cb.successful_requests}")
            print(f"Total Cost (USD): ${cb.total_cost}")
            # Devolver el texto del mensaje
            return corrected_response
    except Exception as e:
        print(e)
        return
    
