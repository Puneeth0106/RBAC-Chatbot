import os
from langchain_astradb import AstraDBVectorStore
from app.services.config import COLLECTION_NAME
from astrapy.info import (
                        CollectionLexicalOptions,
                        CollectionRerankOptions,
                        RerankServiceOptions,
                        )
from langchain_astradb.utils.astradb import HybridSearchMode


#Sparse Retrival
lexical_collection = CollectionLexicalOptions(
    analyzer={
        "tokenizer": {"name": "standard", "args": {}},
        "filters": [
            {"name": "lowercase"},
            {"name": "stop"},
            {"name": "porterstem"},
            {"name": "asciifolding"},
        ],
        "charFilters": [],
    },
    enabled=True,
)

#Reranking 
rerank = CollectionRerankOptions(
    enabled= True,
    service= RerankServiceOptions(
        provider="nvidia",
        model_name="nvidia/llama-3.2-nv-rerankqa-1b-v2"
    ),
)


def get_vector_store(embedding_model):
    vector_store = AstraDBVectorStore(
        collection_name=COLLECTION_NAME,
        embedding=embedding_model,
        collection_lexical=lexical_collection ,
        collection_rerank= rerank,
        hybrid_search= HybridSearchMode.ON, #Default but explicitly turning for future(i.e collection options might change)
        api_endpoint=os.getenv('ASTRA_DB_API_ENDPOINT'),
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
    )
    return vector_store