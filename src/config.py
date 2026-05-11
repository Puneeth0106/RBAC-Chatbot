# Model config
CHAT_MODEL_NAME = "claude-haiku-4-5-20251001"
TEMPERATURE = 0.7
TIMEOUT = 30
MAX_TOKENS = 100
MAX_RETRIES = 6
EMBEDDING_MODEL = "text-embedding-3-large"

# Indexing config
DATA_PATH = '/Users/puneeth/Desktop/my_projects/RBAC-Chatbot/resources/data'
GLOB_PATTERN = "**/*.md"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Vector store config
COLLECTION_NAME = "rbac_docs"
RETRIEVER_K = 5

