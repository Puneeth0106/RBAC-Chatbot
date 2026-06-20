from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas import SingleTurnSample, EvaluationDataset
from ragas.llms import llm_factory
from ragas.run_config import RunConfig
from openai import OpenAI
from pathlib import Path

from app.services.config import EVAL_DATA_PATH
import pandas as pd
import ast
from dotenv import load_dotenv

from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, LLMContextPrecisionWithReference, LLMContextRecall

from app.services.model import embedding_model
from glob import glob

load_dotenv()
evaluator_llm = llm_factory('gpt-4o-mini', client=OpenAI())
embedding_llm= LangchainEmbeddingsWrapper(embedding_model())


silver_files= sorted(glob(f'{EVAL_DATA_PATH}/silver/eval_results_k*.csv'))

def metric_summary():
    rows=[]
    for file in silver_files:
        n= int(Path(file).stem.split('k')[-1])
        df = pd.read_csv(file)
        df['retrieved_contexts'] = df['retrieved_contexts'].apply(ast.literal_eval)
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
            metrics=[LLMContextPrecisionWithReference(), LLMContextRecall()],
            embeddings=embedding_llm,
            llm=evaluator_llm,
            run_config=RunConfig(timeout=120, max_workers=4, max_retries=3)
        ).to_pandas()

        rows.append({'K': n, 'precision': result['llm_context_precision_with_reference'].mean(), 'recall': result['context_recall'].mean()})
    summary_df = pd.DataFrame(rows).sort_values('K')
    Path(f'{EVAL_DATA_PATH}/golden').mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(f'{EVAL_DATA_PATH}/gold/precision_recall_by_k.csv', index=False)


metric_summary()