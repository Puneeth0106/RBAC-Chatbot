from app.services.model import chat_model, embedding_model
from app.services.vectorstore import get_vector_store
from app.services.config import RETRIEVER_K

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

CHAT= chat_model()
EMBEDDING= embedding_model()


# Retriver
def build_retriever(embedding, user_role):
    vector_store= get_vector_store(embedding)
    retriever = vector_store.as_retriever(search_kwargs={"k":RETRIEVER_K , 'filter': {'role':{'$in': [user_role, "general"]}}})
    return retriever

def build_prompt():
    prompt= PromptTemplate.from_template(template=
    """
    Answer the question based only on the context below.
    Context: {context}
    Question: {question}
    """)
    return prompt

def format_output(docs):
    return  "\n\n".join(doc.page_content for doc in docs)

def build_chain(user_role):
    parallel_chain= RunnableParallel(
        {
            'question': RunnablePassthrough(),
            'context': build_retriever(EMBEDDING,user_role) | RunnableLambda(format_output)
        }
    )
    final_chain= parallel_chain | build_prompt() | CHAT | StrOutputParser()
    return final_chain


if __name__== "__main__":
    print(build_chain('engineering').invoke("What CI/CD pipelines does FinSolve use?"))