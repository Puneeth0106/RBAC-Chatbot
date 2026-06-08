# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import os
from astrapy import DataAPIClient
from app.services.config import COLLECTION_NAME

load_dotenv()
db= DataAPIClient(os.environ["ASTRA_DB_APPLICATION_TOKEN"]) \
          .get_database(os.environ["ASTRA_DB_API_ENDPOINT"])

print("before:", db.list_collection_names())
db.drop_collection(COLLECTION_NAME)
print("after: ", db.list_collection_names())