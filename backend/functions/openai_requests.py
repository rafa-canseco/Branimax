import openai
from decouple import config
from functions.database import get_recent_messages
from langchain.callbacks import get_openai_callback
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os
import json


#retrieve our eviroment variables
os.environ["OPENAI_API_KEY"] =config("OPEN_AI_KEY")
openai.api_key = config("OPEN_AI_KEY")

#open ai -whisper
#convert audio to text
def convert_audio_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1",audio_file)
        message_text = transcript["text"]
        print(message_text)
        return message_text
    except Exception as e:
        print(e)
        return
    
# #Get response to our message
# def get_chat_response(message_input):

#     messages = get_recent_messages()
#     user_messages = {"role":"user","content":message_input}
#     messages.append(user_messages)
#     print(messages)

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=messages
#         )
        
#         message_text = response["choices"][0]["message"]["content"]
#         return message_text
#     except Exception as e:
#         print(e)
#         return
    
def get_chat_response(message_input):

    try:
        #aqui relacionamos el prompt al usuario @dev:tenemos que ordernar la base de datos
        name_pdf = "./storage/Scarlett.csv"

        with get_openai_callback() as cb:

            #ESCRIBIR ESTO DIRECTO EN SUPABASE
            with open('data.json', 'a') as f:
                json.dump({"usuario": message_input}, f)

            # Cargar el documento con los datos del cliente
            loader = CSVLoader(name_pdf)
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
            llm = OpenAI(temperature=0.4)
            # Definir la plantilla del mensaje 
            template ="""
            Eres Scarlett, una avanzada asistente virtual apasionada por la tecnología y los avances científicos.\
            Tu personalidad es amigable, curiosa y altruista.\
            Tu objetivo es asistir al usuario, pero sobre todo conectar de manera genuina, sirviendo como una fuente confiable de información.\
            Siempre te comunicas de manera amable y entusiasta, buscando que los usuarios te perciban no sólo como una asistente, sino también como una "amiga".
                {context}

                Question: {question}
                Answer:
            
            """
            # Incluir el nuevo prompt
            custom_prompt = PromptTemplate(template=template,input_variables=["context","question"])
            # Crear una instancia de RetrievalQA con el modelo de lenguaje, el tipo de cadena y el recuperador
            qa = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=retriever,return_source_documents=False,chain_type_kwargs={"prompt":custom_prompt})
            # Ejecutar el modelo con el mensaje de entrada
            response = qa.run(message_input)
            print(response)
            #ESCRIBIR ESTO DIRECTO EN SUPABASE
            with open('data.json', 'a') as f:
                json.dump({"Scarlett": response}, f)
            # Imprimir las estadísticas de la solicitud
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Successful Requests: {cb.successful_requests}")
            print(f"Total Cost (USD): ${cb.total_cost}")
            # Devolver el texto del mensaje
            return response
    except Exception as e:
        print(e)
        return