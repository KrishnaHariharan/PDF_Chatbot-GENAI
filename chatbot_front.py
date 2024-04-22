import os
import streamlit as st
from constants import *
from chatbot_back import *

def answer_user_query(user_question):
    response = st.session_state.conversation({'question': user_question})    
    print(response)
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i%2 == 0:
            with st.chat_message("assistant", avatar='🧑‍💻' ):
                st.markdown(message.content)
        else:
            with st.chat_message("user", avatar='🤖'):
                st.markdown(message.content)
            
    
def main():
    st.set_page_config(page_title="Documind")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("TATA DOCUMIND")
    st.subheader("Chat with your Confidential PDFs")

    #Using the openai key
    os.environ["OPENAI_API_KEY"] = openai_api_key

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload your PDFs", type="pdf", accept_multiple_files=True)
        
    if st.sidebar.button("Upload"):
        with st.spinner("Getting your pdf ready to Query"):
        #get pdf text
            raw_text = get_pdf_text(pdf_docs)

                #get text chunks
            text_chunks = get_text_chunks(raw_text)

                #create vector store
            vector = get_vector_store(text_chunks)

                #Create Conversation Chain
            st.session_state.conversation = get_conversation_chain(vector)
            
            answer_user_query("Give me summary of Uploaded PDFs with each para summarising each uploaded PDF")

    user_query = st.chat_input("Query your PDFs")
    if user_query:
        answer_user_query(user_query)
        
if __name__ == "__main__":
    main()