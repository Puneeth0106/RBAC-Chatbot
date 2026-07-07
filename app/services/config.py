from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Model config
CHAT_MODEL_NAME = "claude-haiku-4-5-20251001"
TEMPERATURE = 0.7
TIMEOUT = 30
MAX_TOKENS = 800
MAX_RETRIES = 6
EMBEDDING_MODEL = "text-embedding-3-large"

# Indexing config
DATA_PATH = Path(__file__).parent.parent.parent.joinpath('resources/data')
EVAL_DATA_PATH= Path(__file__).parent.parent.parent.joinpath('resources/eval')
MANIFEST_DATA_PATH= Path(__file__).parent.parent.parent.joinpath('resources/manifest')
GLOB_PATTERN = "**/*.md"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Vector store config
COLLECTION_NAME = "rbac_docs"
RETRIEVER_K = int(os.getenv("RETRIEVER_K", 6))


#Redis
UPSTASH_REDIS_REST_URL= os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN= os.getenv("UPSTASH_REDIS_REST_TOKEN")
SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", 86400))