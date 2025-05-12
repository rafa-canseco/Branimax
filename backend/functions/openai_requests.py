# from openai import OpenAI
from decouple import config
from langchain_community.callbacks import get_openai_callback
from langchain_community.document_loaders import CSVLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import SupabaseVectorStore
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.messages import HumanMessage, SystemMessage
from functions.querys_db import getPromtByCompany,getUrlCsvForContext,getCompanyId,getPromtByCompany
import os
import re
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from supabase.client import Client, create_client
from langchain.schema import Document
import unicodedata

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

supabase: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)

embeddings = OpenAIEmbeddings(request_timeout=400)
os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
OpenAI.api_key = config("OPENAI_API_KEY")
client = OpenAI()
llm = ChatOpenAI(temperature=0,model="gpt-4o")
output_parser = StrOutputParser()

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
    instruction = f"Sintetiza la siguiente nota periodística con máximo 100 palabras: {text}"
    messages = [HumanMessage(content=instruction)]
    response = llm.invoke(messages)
    print(response.content)
    return response.content 

def generate_tweet_simple(prompt):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}")
    ])

    chain = prompt | llm | output_parser
    response = chain.invoke({"input": "genera un tweet interesante debe obligatoriamente ser menor a 120 caracteres, escribe el tweet sin incluir apóstrofes como si estuvieras haciendo una cita, solo regresa el texto simple.,no pongas estos signos en el tweet ("") o ('') debe ser solo el texto."})
    return response

def generate_response(prompt, tweet_original,indicacion,hashtag):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}")
    ])
    
    chain = prompt | llm | output_parser
    response = chain.invoke({"input": f"genera un tweet respuesta a este tweet {tweet_original} siguiendo esta indicación : {indicacion} y usa el siguiente hash : {hashtag},debe obligatoriamente ser menor a 140 caracteres,  escribe el tweet sin incluir apóstrofes como si estuvieras haciendo una cita, solo regresa el texto simple.,no pongas estos signos en el tweet ("") o ('') debe ser solo el texto.: "})
    print(response)
    return response


def generate_resume(lista_de_tweets):
    prompt = "Eres un bot de twitter diseñado para resumir los tweets de un usuario dado y dar los insights mas importantes para sus publicaciones, debes dar la información clara y de manera digerida "
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}")
    ])
    
    chain = prompt | llm | output_parser
    response = chain.invoke({"input": f"Aquí tienes una lista de tweets recientes de un usuario. Por favor, analízalos y proporciona un resumen conciso que destaque los temas principales y los puntos más importantes de lo que el usuario ha estado discutiendo:: {lista_de_tweets}"})
    return response

def generate_tweet(prompt, topic, hashtag):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}")
    ])

    chain = prompt | llm | output_parser
    response = chain.invoke({"input": f"genera un tweet interesante sobre el siguiente tema {topic} asegurate de incluir los siguientes {hashtag} ,debe obligatoriamente ser menor a 120 caracteres, escribe el tweet sin incluir apóstrofes como si estuvieras haciendo una cita, solo regresa el texto simple.,no pongas estos signos en el tweet ("") o ('') debe ser solo el texto."})
    return response

def generate_tweet_url(prompt, topic, hashtag,url):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}")
    ])

    chain = prompt | llm | output_parser
    response = chain.invoke({"input": f"genera un tweet interesante sobre el siguiente tema {topic} asegurate de incluir los siguientes {hashtag} y {url},debe obligatoriamente ser menor a 120 caracteres, escribe el tweet sin incluir apóstrofes como si estuvieras haciendo una cita, solo regresa el texto simple.,no pongas estos signos en el tweet ("") o ('') debe ser solo el texto."})
    return response

def clean_text(text):
    if not text:
        return ""
    # Eliminar caracteres nulos
    text = text.replace('\x00', '')
    # Codificar y decodificar para eliminar caracteres no UTF-8
    text = text.encode('utf-8', errors='ignore').decode('utf-8')
    # Normalizar unicode
    text = unicodedata.normalize('NFKD', text)
    return text

def generateEmbeddigs():
    try:
        pdf = os.path.join(os.path.dirname(__file__), '..', 'storage', 'agro.pdf')

        loader = PyPDFLoader(pdf)
        documents = loader.load()
        
        # Limpiar el texto de cada documento
        cleaned_documents = []
        for doc in documents:
            cleaned_text = clean_text(doc.page_content)
            cleaned_doc = Document(page_content=cleaned_text, metadata=doc.metadata)
            cleaned_documents.append(cleaned_doc)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
        docs = text_splitter.split_documents(cleaned_documents)

        vector_store = SupabaseVectorStore.from_documents(
            docs,
            embeddings,
            client=supabase,
            table_name="documents_cartesiano",
            query_name="match_documents_cartesiano",
            chunk_size=500,
        )
        print("Embeddings creados y guardados exitosamente")
    except Exception as e:
        print(f"Error al crear embeddings: {e}")

def retrieveContext():
    vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase,
        table_name="documents",
        query_name="match_documents",
    )
    return vector_store

def retrieveContextRestaurants():
    vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase,
        table_name="documents_restaurants",
        query_name="match_documents_new",
    )
    return vector_store

def retrieveContextCartesianoSpa():
    vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase,
        table_name="documents_cartesiano",
        query_name="match_documents_cartesiano",
    )
    return vector_store

def retrieveContextAlcazar():
    vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase,
        table_name="documentsalcazar",
        query_name="match_documents_alcazar"
    )
    return vector_store

def retrieveContextPromuevo():
    vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase,
        table_name="documents_promuevo",
        query_name="match_documents_promuevo"
    )
    return vector_store

def retrieveContextUniversidad():
    vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase,
        table_name="documents_universidad",
        query_name="match_documents_universidad"
    )
    return vector_store

def get_chat_response_vectorized(message_input, id, template):
    print(id)
    if id == 17:
        context = retrieveContextAlcazar()
    elif id == 19:
        context = retrieveContextCartesianoSpa()
    elif id == 15:
        context = retrieveContextRestaurants()
    elif id == 9:
        context = retrieveContextPromuevo()
    elif id == 20:
        context = retrieveContextUniversidad()
    else:
        context = retrieveContext()
    
    retriever = context.as_retriever(search_type="similarity", search_kwargs={"k": 2})

    customPrompt = PromptTemplate(template=template, input_variables=["context", "question"])
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=False, chain_type_kwargs={"prompt": customPrompt})
    response = qa.invoke({"query": message_input})
    return response["result"]

generateEmbeddigs()