from functions.querys_db import getPromtByCompany,getConversationSaved,getUrlCsvForContext,getCompanyId
from langchain_community.callbacks import get_openai_callback
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from functions.openai_requests import fix_encoding,clean_response_text
from utils.currentDate import get_full_current_date
from utils.history import get_history_parse
from langchain_openai import ChatOpenAI


def get_context(message_input, id, state):
    csv = getUrlCsvForContext(id)

    with get_openai_callback() as cb:
        # Cargar el documento con los datos del cliente
        history = get_history_parse(state)
        now_date = get_full_current_date()
        loader = PyPDFLoader(csv)
        documents = loader.load()

        # Dividir el documento en fragmentos
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        # Crear los embeddings
        embeddings = OpenAIEmbeddings()
        # Crear el índice de vectores
        db = Chroma.from_documents(texts, embeddings)
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
        # Iniciar el modelo de lenguaje, definir la temperatura y el modelo
        llm = ChatOpenAI(model = "gpt-4o")
        # Definir la plantilla del mensaje 
        template = """Como experto en ventas con aproximadamente 15 años de experiencia en embudos de ventas y generación de leads, tu tarea es mantener una conversación agradable, responder a las preguntas del cliente sobre nuestros productos y, finalmente, guiarlos para reservar una cita. Tus respuestas deben basarse únicamente en el contexto proporcionado:

        ### DÍA ACTUAL
        {CURRENT_DAY}

        ### HISTORIAL DE CONVERSACIÓN (Cliente/Vendedor)
        {HISTORY}

        ### BASE DE DATOS
        {{context}}

        Para proporcionar respuestas más útiles, puedes utilizar la información proporcionada en la base de datos. El contexto es la única información que tienes. Ignora cualquier cosa que no esté relacionada con el contexto.

        ### EJEMPLOS DE RESPUESTAS IDEALES:

        - Por supuesto, tenemos eso y además...
        - Claro, puedo ayudarte con eso. ¿Te gustaría que te explique más detalles?
        - Entiendo perfectamente. Aquí tienes la información que necesitas...
        - Definitivamente, puedo ayudarte con eso.
        - ¡Genial! Te proporcionaré todos los detalles a continuación...
        - Claro, aquí tienes lo que buscas y algunas recomendaciones adicionales...
        - Sin problema, te puedo guiar en eso. ¿Te gustaría saber más sobre...?


        Respuesta útil adecuadas para enviar por WhatsApp (en español):

        Question: {{question}}  
        Answer:
        """
        
        # Crear un nuevo template con los valores de history y now_date
        custom_template = template.format(CURRENT_DAY=now_date, HISTORY=history)
        # Incluir el nuevo prompt
        custom_prompt = PromptTemplate(template=custom_template, input_variables=["context","question"])
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=False, chain_type_kwargs={"prompt": custom_prompt})
        response = qa.invoke({"query":message_input})
        print(response['result'])
        return response['result']