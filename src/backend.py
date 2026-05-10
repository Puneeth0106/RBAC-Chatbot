from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

#ChatModel
model = init_chat_model(
    "claude-haiku-4-5-20251001",
    # Kwargs passed to the model:
    temperature=0.7,
    timeout=30,
    max_tokens=100,
    max_retries=6,  # Default; increase for unreliable networks
)



#Indexing
loader= DirectoryLoader(
    path='/Users/puneeth/Desktop/my_projects/RBAC-Chatbot/resources/data',
    glob= "**/*.md",
    loader_cls=TextLoader
)

docs= loader.load()

#Splitting
headers_to_split_on = [
      ("#", "Header 1"),
      ("##", "Header 2"),
      ("###", "Header 3"),
  ]


md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
char_splitter= RecursiveCharacterTextSplitter(chunk_size= 500,chunk_overlap=50)


def splitting_docs(docs):
    md_chunks=[]
    for doc in docs:
        md_chunks.extend(md_splitter.split_text(doc.page_content))
    return md_chunks

chunks= splitting_docs(docs)
final_chunks = char_splitter.split_documents(chunks)


#Vector Store

embedding_model= OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = AstraDBVectorStore(
    collection_name="rbac_docs",
    embedding=embedding_model,
    api_endpoint=os.getenv('ASTRA_DB_API_ENDPOINT'),
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
)



document_ids = vector_store.add_documents(documents=final_chunks)


prompt= PromptTemplate.from_template(template=
  """
  Answer the question based only on the context below.

  Context: {context}

  Question: {question}
  """)



# Retriver
retriever = vector_store.as_retriever(search_kwargs={"k": 1})


output_parser = StrOutputParser()


def format_output(docs):
    return  "\n\n".join(doc.page_content for doc in docs)



parallel_chain= RunnableParallel(
    {
        'question': RunnablePassthrough(),
        'context': retriever | RunnableLambda(format_output)
    }
)

final_chain= parallel_chain | prompt | model | output_parser


if __name__== "__main__":
    print(final_chain.invoke("How many leaves can a employee get"))