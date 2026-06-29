import hashlib
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from app.services.config import DATA_PATH,GLOB_PATTERN, CHUNK_OVERLAP,CHUNK_SIZE, MANIFEST_DATA_PATH
from app.services.vectorstore import get_vector_store
from app.services.model import embedding_model
from pathlib import Path
import json


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



def compute_hash(path):
    data= Path(path).read_bytes()
    hash= hashlib.md5(data).hexdigest()
    return hash


def load_manifest(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_manifest(manifest,path):
    with open(path, mode='w') as f:
        json.dump(manifest,f)


def refresh_index(path, vector_store):
    MANIFEST_DATA_PATH.mkdir(parents=True, exist_ok=True)
    manifest= load_manifest(MANIFEST_DATA_PATH / "index_manifest.json")
    for file in Path(path).rglob('*md'):
        role= Path(file).parent.name
        hash_file= compute_hash(Path(file))
        # Check the computed hash is inside the manifest; if it is new we add them if changed we index them again
        if str(file) not in manifest or manifest[str(file)] != hash_file:
            manifest[str(file)]= hash_file
            #Loading docs takes Directory loader so not using it and just using TextLoader
            docs = TextLoader(str(file)).load()
            chunks = splitting_docs(docs)
            chunks = tag_chunks(chunks, role)
            vector_store.add_documents(chunks)
    
    save_manifest(manifest,MANIFEST_DATA_PATH.joinpath("index_manifest.json"))





if __name__== "__main__":
    vector_store = get_vector_store(embedding_model())
    refresh_index(DATA_PATH,vector_store)


