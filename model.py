import os
import openai
import sys
import numpy as np
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langdetect import detect

def getResponse(question: str) -> str:
    """
    A repeated implementation of the langchain code in Week 5
    This code is purposely built to be inefficient! 
    Refer to project requirements and Week 5 Lab if you need help
    """

    load_dotenv("./.env")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LANGCHAIN_API_KEY = os.getenv("LANGSMITH_API_KEY")

    
    openai.api_key = OPENAI_API_KEY
    

    loader = PyPDFDirectoryLoader("./docs/")
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )

    splits = text_splitter.split_documents(pages)

    # Your experiment can start from this code block which loads the vector store into variable vectordb
    embedding = OpenAIEmbeddings()

    # Reference https://github.com/hwchase17/chroma-langchain/blob/master/persistent-qa.ipynb
    persist_directory = './docs/vectordb'

    # Perform embeddings and store the vectors
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory # Writes to local directory in G Drive
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key='question',
        output_key='answer'
    )

    # Code below will enable tracing so we can take a deeper look into the chain
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
    os.environ["LANGCHAIN_PROJECT"] = "Chatbot"

    # Define parameters for retrival
    retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 5})

    # Define llm model

    llm_name = "gpt-3.5-turbo-16k"
    llm = ChatOpenAI(model_name=llm_name, temperature=0)

     # Detect language of the question
    try:
        lang = detect(question)
    except:
        lang = 'en'  # default to English if detection fails

# Adjust the template based on detected language
    if lang == 'bn':  # 'bn' is the code for Bangla
        template = """You are a chatbot helping new staff and volunteers to know more about the migrant workers’ medical, dental and mental coverage in Singapore and also to help bridge the gap between new staff and volunteers and migrant workers. Always say \n\nI hope this answers your question and if our previous response did not address your question adequately, please feel free to reach out to HealthServe at +65 3157 4450 (general enquiries) or email them info@healthserve.org.sg at the end of the answer. Use the following piece of context to answer the question at the end.
        {context}
        Question: {question}
        Answer in Bangla:"""

    elif lang == 'ta':  # Tamil
        template = """You are a chatbot helping new staff and volunteers to know more about the migrant workers’ medical, dental and mental coverage in Singapore and also to help bridge the gap between new staff and volunteers and migrant workers. Always say \n\nI hope this answers your question and if our previous response did not address your question adequately, please feel free to reach out to HealthServe at +65 3157 4450 (general enquiries) or email them info@healthserve.org.sg at the end of the answer. Use the following piece of context to answer the question at the end.
        {context}
        Question: {question}
        Answer in Tamil:"""

    else:  # default to English
        template = """You are a chatbot helping new staff and volunteers to know more about the migrant workers’ medical, dental and mental coverage in Singapore and also to help bridge the gap between new staff and volunteers and migrant workers. Always say \n\nI hope this answers your question and if our previous response did not address your question adequately, please feel free to reach out to HealthServe at +65 3157 4450 (general enquiries) or email them info@healthserve.org.sg at the end of the answer. Use the following piece of context to answer the question at the end.
        {context}
        Question: {question}
        Helpful Answer:"""


    your_prompt = PromptTemplate.from_template(template)

    # Execute chain
    qa = ConversationalRetrievalChain.from_llm(
        llm,
        combine_docs_chain_kwargs={"prompt": your_prompt},
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
        memory=memory
    )

    # Evaluate your chatbot with questions
    result = qa({"question": question})

    print(result)
    return result['answer']