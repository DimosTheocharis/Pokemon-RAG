import streamlit as st
from utils import responseGenerator

st.title("Pokemon RAG")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    chatMessage = st.chat_message(message["role"])
    chatMessage.markdown(message["content"])

print('eo')


prompt = st.chat_input("Say something")
if (prompt):
    # Display user message in chat message container
    chatMessage = st.chat_message("user")
    chatMessage.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Display assistant response in chat message container
    chatMessage = st.chat_message("assistant")
    response = chatMessage.write_stream(responseGenerator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
