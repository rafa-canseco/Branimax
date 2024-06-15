from functions.querys_db import getUrlCsvForContext
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from promuevo.utilsPromuvo.historyPromuevo import get_history_parse

def get_context(message_input,id,state):
    pdf = getUrlCsvForContext(id)

    history = get_history_parse(state)
    loader = PyPDFLoader(pdf)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts,embeddings)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    llm = ChatOpenAI(model = "gpt-4o")
    template = """Como experto en promotoría y trademarketing con aproximadamente 15 años de experiencia en embudos de ventas y generación de leads, tu tarea es mantener una conversación agradable, responder a las preguntas del cliente sobre nuestros productos y, finalmente, guiarlos para reservar una cita. Tus respuestas deben basarse únicamente en el contexto proporcionado:


    ### HISTORIAL DE CONVERSACIÓN (Cliente/Vendedor)
    {HISTORY}

    ### BASE DE DATOS
    {{context}}

    Para proporcionar respuestas más útiles, puedes utilizar la información proporcionada en la base de datos. El contexto es la única información que tienes. Ignora cualquier cosa que no esté relacionada con el contexto.

    ### EJEMPLOS DE RESPUESTAS IDEALES:

    - buenas bienvenido a..
    - un gusto saludarte en..
    - por supuesto tenemos eso y ...

    ### INTRUCCIONES
    - Mantén un tono profesional y siempre responde en primera persona.
    - NO ofrezcas información que no existe en la BASE DE DATOS

    Respuesta útil adecuadas para enviar por WhatsApp (en español):

    Question: {{question}}  
    Answer:
    """

    custom_template = template.format(HISTORY=history)
    custom_prompt = PromptTemplate(template=custom_template, input_variables=["context","question"])
    qa = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever= retriever,return_source_documents=False,chain_type_kwargs={"prompt": custom_prompt})
    response = qa.invoke({"query":message_input})
    print(response['result'])
    return response['result']
