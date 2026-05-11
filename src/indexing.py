from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from src.config import DATA_PATH,GLOB_PATTERN, CHUNK_OVERLAP,CHUNK_SIZE

def loading_docs(path):
    loader= DirectoryLoader(
        path= path ,
        glob= GLOB_PATTERN,
        loader_cls=TextLoader
    )
    docs= loader.load()
    return docs


def splitting_docs(docs):
    #Splitting
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    md_chunks=[]
    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    char_splitter= RecursiveCharacterTextSplitter(chunk_size= CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)
    for doc in docs:
        md_chunks.extend(md_splitter.split_text(doc.page_content))
    final_chunks = char_splitter.split_documents(md_chunks)
    return final_chunks





