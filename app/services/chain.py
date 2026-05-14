from app.services.model import chat_model, embedding_model
from app.services.vectorstore import get_vector_store
from app.services.config import RETRIEVER_K

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import trim_messages
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_community.chat_message_histories import ChatMessageHistory

from operator import itemgetter

CHAT= chat_model()
EMBEDDING= embedding_model()

def build_retriever(embedding, user_role):
    vector_store= get_vector_store(embedding)
    retriever = vector_store.as_retriever(search_kwargs={"k":RETRIEVER_K , 'filter': {'role':{'$in': [user_role, "general"]}}})
    return retriever

#Memory
store= {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory() #Holds multi thread messages in a list can be replaced with Redis
    return store[session_id]


def build_prompt():
    prompt= PromptTemplate.from_template(template=
    """
    Answer the question based only on the context below.
    Chat history : {chat_history}
    Context: {context}
    Question: {question}
    """)
    return prompt

def format_output(docs):
    return  "\n\n".join(doc.page_content for doc in docs)

def build_chain(user_role):

    #Trimmer for making sure the context history is below 1000 tokens before passing into LLM
    trimmer= trim_messages(
        max_tokens= 1000,
        strategy = 'last',
        token_counter=CHAT,
        include_system=True,
        allow_partial=False)
        
    parallel_chain= RunnableParallel(
        {
            'question': itemgetter('question'), # itemgetter is like key finder inside dictionary
            'context': itemgetter('question') | build_retriever(EMBEDDING,user_role) | RunnableLambda(format_output),
            'chat_history' : itemgetter('chat_history') | trimmer
        }
    )

    final_chain= parallel_chain | build_prompt() | CHAT | StrOutputParser()
    return RunnableWithMessageHistory(
        final_chain,
        get_session_history, #Search/retrive ChatMessageHistory via Session-ID
        input_messages_key= 'question', #labels that tells wher to look 'question' in the dictionary
        history_messages_key= "chat_history" #labels that tells wher to look  'chat-history' in the dictionary
    )


if __name__== "__main__":
    print(build_chain('engineering').invoke("What CI/CD pipelines does FinSolve use?"))