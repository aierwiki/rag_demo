import os
import time
import joblib
import numpy as np
import gradio as gr
from openai import OpenAI
from langchain.schema import AIMessage, HumanMessage
from zhipuai import ZhipuAI
from loguru import logger

EMBEDDING_API_KEY = os.getenv("ZHIPU_API_KEY", None)
if EMBEDDING_API_KEY is None:
    raise ValueError("Please set the ZHIPU_API_KEY environment variable.")

embedding_client = ZhipuAI(api_key=EMBEDDING_API_KEY)


API_KEY = os.getenv("DEEPSEEK_API_KEY", None)
if API_KEY is None:
    raise ValueError("Please set the DEEPSEEK_API_KEY environment variable.")


client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")


def recall_relevent_knowledge(query:str):
    path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(path, "data")
    vector_db = joblib.load(os.path.join(data_path, "vector_db.pkl"))
    snippets = joblib.load(os.path.join(data_path, "snippets.pkl"))

    # 获取query对应的向量
    response = embedding_client.embeddings.create(
            model="embedding-2", #填写需要调用的模型名称
            input=query,
        )
    query_emb = np.array(response.data[0].embedding)
    
    # 从向量数据库里面找到最相关的知识
    sim_score = np.dot(vector_db, query_emb)
    max_idx = np.argmax(sim_score)
    snippet = snippets[max_idx]

    return snippet


def predict(message, history):
    relevant_knowledge = recall_relevent_knowledge(message)
    logger.info(f"Relevant knowledge: {relevant_knowledge}")

    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    # history_openai_format.append({"role": "user", "content": message})
    prompt = f"""我的问题是：{message}, 相关的知识是：{relevant_knowledge}。请回答我的问题。"""
    history_openai_format.append({"role": "user", "content": prompt})
  
    response = client.chat.completions.create(model='deepseek-chat',
            messages= history_openai_format,
            temperature=1.0,
            stream=True)

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
              partial_message = partial_message + chunk.choices[0].delta.content
              yield partial_message

gr.ChatInterface(predict).launch()