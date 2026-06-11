from setup import setupFrontend
setupFrontend()


import streamlit as st
from llama_index.core import VectorStoreIndex 
from middleware.middleman import Middleware


st.title("Pokemon RAG")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    chatMessage = st.chat_message(message["role"])
    chatMessage.markdown(message["content"])




@st.cache_resource(show_spinner=True)
def loadData() -> VectorStoreIndex:
    return Middleware.createIndex()


index: VectorStoreIndex = loadData()
queryEngine = index.as_query_engine(similarity_top_k=10)




prompt = st.chat_input("Say something")
if (prompt):
    # Display user message in chat message container
    chatMessage = st.chat_message("user")
    chatMessage.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Display assistant response in chat message container
    chatMessage = st.chat_message("assistant")
    response = queryEngine.query(prompt)
    if (response):
        chatMessage.markdown(response.response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.response})
