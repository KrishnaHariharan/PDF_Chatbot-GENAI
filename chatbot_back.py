from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import streamlit as st

#This function is for extracting 
#texts from the PDFs
def get_pdf_text(pdf):
    text = ""
    for file in pdf:
        pdf_Reader = PdfReader(file)
        for page in pdf_Reader.pages:
            text += page.extract_text()
    return text

#This function is for breaking
#the text int0 small chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(chunk):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(chunk, embeddings)
    return vectorstore


def get_conversation_chain(vector):
    llm = ChatOpenAI()
    memory_made = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation = ConversationalRetrievalChain.from_llm(llm = llm, retriever = vector.as_retriever(), memory = memory_made )
    return conversation

    
    
