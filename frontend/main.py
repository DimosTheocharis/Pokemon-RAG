import streamlit as st
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings 
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

import time, os, json

st.title("Pokemon RAG")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    chatMessage = st.chat_message(message["role"])
    chatMessage.markdown(message["content"])


def file_metadata_func(file_path: str):
    pokemonName = ('r' + file_path).split('\\')[-1][:-4]
    if os.path.isfile(f'../backend/metadata/{pokemonName}.json'):
        with open(f'../backend/metadata/{pokemonName}.json', 'r') as f:
            metadata = json.load(f)
            return metadata
    else:
        print(f'This is not a file: {f'../backend/metadata/{pokemonName}.json'}')

    return {}

@st.cache_resource(show_spinner=True)
def loadData():
    documents = SimpleDirectoryReader('../backend/data', file_metadata=file_metadata_func).load_data()
    
    # Set up the LLM and embedding model
    Settings.llm = Ollama(
        model="llama3.1:8b",
        request_timeout=60,
        context_window=8000,
        system_prompt = """
            You are a Pokemon assistant.
            You MUST answer ONLY using the provided documents.
            Do NOT say you don't know if the answer exists in the documents.
            If the user misspells a Pokémon name, map it to the closest Pokémon in the provided documents.
            If the correct Pokémon exists in the documents, always answer using it.
            You can include metadata when needed.
        """
    )

    Settings.embed_model = OllamaEmbedding(
        model_name="bge-m3"
    )

    index = VectorStoreIndex.from_documents(documents)
    return index


index = loadData()
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
