from app.services.config import DATA_PATH
from app.services.indexing import loading_docs
from app.services.model import chat_model, embedding_model
from ragas.testset import TestsetGenerator
import pandas as pd

generator= TestsetGenerator.from_langchain(chat_model(),embedding_model())


frames= []

for role in ["engineering", "finance", "marketing","hr", "general"]:
    path= f'{DATA_PATH}/{role}'
    docs=loading_docs(path)
    testset= generator.generate_with_langchain_docs(docs,testset_size=10)
    df = testset.to_pandas()
    df['role']= role
    frames.append(df)

pd.concat(frames).to_csv(f"resources/eval/bronze/golden_raw.csv", index= False)

