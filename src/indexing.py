from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from src.config import DATA_PATH,GLOB_PATTERN, CHUNK_OVERLAP,CHUNK_SIZE
from langchain_astradb import AstraDBVectorStore
from src.config import COLLECTION_NAME
from src.model import embedding_model
import os

def loading_docs(path):
    loader= DirectoryLoader(
        path= path ,
        glob= GLOB_PATTERN,
        loader_cls=TextLoader
    )
    docs= loader.load()
    return docs


#Splitting
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
char_splitter= RecursiveCharacterTextSplitter(chunk_size= CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)



def splitting_docs(docs):
    md_chunks=[]
    for doc in docs:
        md_chunks.extend(md_splitter.split_text(doc.page_content))
    final_chunks = char_splitter.split_documents(md_chunks)
    return final_chunks



if __name__== "__main__":

    vector_store = AstraDBVectorStore(
    collection_name=COLLECTION_NAME,
    embedding=embedding_model(),
    api_endpoint=os.getenv('ASTRA_DB_API_ENDPOINT'),
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"))

    roles= ["engineering", "finance", "marketing","hr", "general"]

    for role in roles:
        path= f"{DATA_PATH}/{role}"
        docs= loading_docs(path)
        chunks= splitting_docs(docs)
        for chunk in chunks:
            chunk.metadata["role"] = role

        vector_store.add_documents(chunks)

