from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from app.services.config import DATA_PATH,GLOB_PATTERN, CHUNK_OVERLAP,CHUNK_SIZE
from app.services.vectorstore import get_vector_store
from app.services.model import embedding_model
from pathlib import Path

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
        chunks = md_splitter.split_text(doc.page_content)
        for  chunk in chunks:
            if 'source' in doc.metadata:
                chunk.metadata["source"] = str(Path(doc.metadata['source']).relative_to(DATA_PATH))
        md_chunks.extend(chunks)
    final_chunks = char_splitter.split_documents(md_chunks)
    return final_chunks


def tag_chunks(chunks,role):
    for chunk in chunks:
        chunk.metadata["role"] = role
    return chunks



if __name__== "__main__":

    vector_store = get_vector_store(embedding_model())
    roles= ["engineering", "finance", "marketing","hr", "general"]
    for role in roles:
        path= f"{DATA_PATH}/{role}"
        docs= loading_docs(path)
        chunks= splitting_docs(docs)
        chunks= tag_chunks(chunks, role) #datapath is inherieted directly
        vector_store.add_documents(chunks)

