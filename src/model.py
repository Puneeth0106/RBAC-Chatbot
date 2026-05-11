from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_openai.embeddings import OpenAIEmbeddings
from src.config import CHAT_MODEL_NAME, TEMPERATURE, TIMEOUT,MAX_RETRIES,MAX_TOKENS,EMBEDDING_MODEL

def chat_model():
    load_dotenv()
    model = init_chat_model(
        CHAT_MODEL_NAME,
        temperature=TEMPERATURE,
        timeout=TIMEOUT,
        max_tokens=MAX_TOKENS,
        max_retries=MAX_RETRIES,  
    )
    return model

def embedding_model():
    load_dotenv()
    embedding_model= OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return embedding_model
