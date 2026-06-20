from ragas import SingleTurnSample, EvaluationDataset
from ragas.llms import llm_factory
from ragas.run_config import RunConfig
from openai import OpenAI

from app.services.config import EVAL_DATA_PATH
import pandas as pd
import ast
from dotenv import load_dotenv

from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, LLMContextPrecisionWithReference, LLMContextRecall

load_dotenv()
evaluator_llm = llm_factory('gpt-4o-mini', client=OpenAI())




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

result= evaluate(
    dataset=raga_eval_dataset,
    metrics=[Faithfulness(), AnswerRelevancy(), LLMContextPrecisionWithReference(), LLMContextRecall()],
    llm=evaluator_llm,
    run_config=RunConfig(timeout=120, max_workers=4, max_retries=3)
).to_pandas()

result.to_csv(f'{EVAL_DATA_PATH}/ragas_metric_scores.csv', index=False)



