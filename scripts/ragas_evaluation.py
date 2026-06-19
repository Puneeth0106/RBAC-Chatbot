from ragas import SingleTurnSample, EvaluationDataset

from ragas.llms import LangchainLLMWrapper

from app.services.config import EVAL_DATA_PATH
import pandas as pd
import ast

from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, LLMContextPrecisionWithReference, LLMContextRecall

from app.services.config import CHAT_MODEL_NAME, TEMPERATURE, TIMEOUT,MAX_RETRIES
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

#Configure the LLM seperately the default chat_model has token limit issue so initiating a new llm with 4096 tokens

load_dotenv()
model = init_chat_model(
    CHAT_MODEL_NAME,
    temperature=TEMPERATURE,
    timeout=TIMEOUT,
    max_tokens=8000,
    max_retries=MAX_RETRIES,  
)

evaluator_llm = LangchainLLMWrapper(model)




#Load Eval Dataset
df = pd.read_csv(f'{EVAL_DATA_PATH}/eval_results.csv')
df['retrieved_contexts'] = df['retrieved_contexts'].apply(ast.literal_eval)
df['reference_contexts'] = df['reference_contexts'].apply(ast.literal_eval)

samples=[]

for i,row in df.iterrows():
    samples.append(
        SingleTurnSample(
            user_input= row['user_input'],
            response = row['response'],
            retrieved_contexts= row['retrieved_contexts'],
            reference= row['reference']
                     ))


raga_eval_dataset = EvaluationDataset(samples= samples)

result= evaluate(dataset=raga_eval_dataset,  metrics=[Faithfulness(), AnswerRelevancy(), LLMContextPrecisionWithReference(), LLMContextRecall()], llm=evaluator_llm).to_pandas()

result.to_csv(f'{EVAL_DATA_PATH}/ragas_metric_scores.csv', index=False)



