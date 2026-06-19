
from app.services.chain import build_chain
from app.services.config import EVAL_DATA_PATH
import pandas as pd
import asyncio


golden_df= pd.read_csv(f'{EVAL_DATA_PATH}/golden_raw.csv')
print(golden_df.head(2))

response= []
retrieved_contexts_list= []

async def run_eval():
    for i,row in golden_df.iterrows():
        page_content_list = []
        response_string = ''
        async for event in build_chain(row['role']).astream_events(
            {'question':row['user_input']},
            config= {'configurable': {'session_id': f'eval{i}'}},
            version= 'v2'
            ):
            kind= event['event']
            if kind== "on_retriever_end":
                docs= event['data']['output']
                for doc in docs:
                    page_content_list.append(doc.page_content)
            
            if kind== "on_chat_model_stream":
                token= event['data']['chunk'].content
                response_string +=token
        response.append(response_string)
        retrieved_contexts_list.append(page_content_list)


asyncio.run(run_eval())

golden_df['response']= response
golden_df['retrieved_contexts']= retrieved_contexts_list

print(golden_df.head(2))

golden_df.to_csv(f'{EVAL_DATA_PATH}/eval_results.csv', index=False)