import os
from langchain_astradb import AstraDBVectorStore
from app.services.config import COLLECTION_NAME


def get_vector_store(embedding_model):
    vector_store = AstraDBVectorStore(
        collection_name=COLLECTION_NAME,
        embedding=embedding_model,
        api_endpoint=os.getenv('ASTRA_DB_API_ENDPOINT'),
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
    )
    return vector_store