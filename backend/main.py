from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import os, json
from pathlib import Path

BACKEND_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = os.path.join(BACKEND_DIRECTORY, 'data')
METADATA_DIRECTORY = os.path.join(BACKEND_DIRECTORY, 'metadata')

def file_metadata_func(file_path: str):
    pokemonName = ('r' + file_path).split('\\')[-1][:-4]
    if os.path.isfile(os.path.join(METADATA_DIRECTORY, f'{pokemonName}.json')):
        with open(os.path.join(METADATA_DIRECTORY, f'{pokemonName}.json'), 'r') as f:
            metadata = json.load(f)
            return metadata
    else:
        print(f'This is not a file: {os.path.join(METADATA_DIRECTORY, f'{pokemonName}.json')}')

    return {}

def createIndex() -> VectorStoreIndex:
    '''
        Create a VectorStoreIndex from documents in the './backend/data' directory, 
        using Ollama as the LLM and embedding model.
    '''
    documents = SimpleDirectoryReader(DATA_DIRECTORY, file_metadata=file_metadata_func).load_data()

    # Set up the LLM and embedding model
    Settings.llm = Ollama(
        model="llama3.1:8b",
        request_timeout=120,
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