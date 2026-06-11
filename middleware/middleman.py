from llama_index.core import VectorStoreIndex
from backend.main import createIndex

class Middleware:
    @staticmethod
    def createIndex() -> VectorStoreIndex:
        return createIndex()
