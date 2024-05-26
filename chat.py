import os
import time
import re
import joblib
import jinja2
from typing import List, Dict
import numpy as np
import gradio as gr
from openai import OpenAI
from langchain.schema import AIMessage, HumanMessage
from zhipuai import ZhipuAI
from loguru import logger
from tools import query_history_k_data_plus
from pprint import pprint


EMBEDDING_API_KEY = os.getenv("ZHIPU_API_KEY", None)
if EMBEDDING_API_KEY is None:
    raise ValueError("Please set the ZHIPU_API_KEY environment variable.")

embedding_client = ZhipuAI(api_key=EMBEDDING_API_KEY)


def load_system_prompt():
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, "templates", "system.tmpl"), "r") as f:
        template = jinja2.Template(f.read())
        prompt = template.render({})
    return prompt
    

SYS_PROMPT = load_system_prompt()
GLOBAL_FUNCS = {"query_history_k_data_plus": query_history_k_data_plus}


API_KEY = os.getenv("DEEPSEEK_API_KEY", None)
if API_KEY is None:
    raise ValueError("Please set the DEEPSEEK_API_KEY environment variable.")


client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")


def call_chatbot(messages:List[Dict[str, str]]):
    pprint(messages)
    response = client.chat.completions.create(model='deepseek-chat',
            messages= messages,
            temperature=1.0,
            stream=True)
    return response


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


def check_and_execute_action_code(msg:str) -> str:
    """
    ```
    def action() -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ```
    用正则表达式将msg中的python代码提取出来，然后执行这段代码，返回执行结果。
    """
    if "def action()" not in msg:
        return None
    code_pattern = r'```(?:python\n)?(.*def action.*?)```'
    match = re.search(code_pattern, msg, re.DOTALL)
    if match is None:
        logger.error(f"No python code found in the message. {msg}")
        return None
    code = match.group(1)
    logger.info(f"Extracted code: ```\n{code}\n```")
    global_vars = {**GLOBAL_FUNCS}
    try:
        exec(code, global_vars)
        info = global_vars['action']()
        prompt = f"执行action()获取到的信息如下：{info}"
    except Exception as e:
        logger.error(f"Failed to execute the action code. {e}")
        prompt = f"执行action()时出错：{e}"
    return prompt

def test_execute_action_code():
    msg = """
    请帮我执行如下代码：
    ```python
import datetime
def action() -> str:
    return str(datetime.datetime.now())
    ```
    """
    code = """
import datetime
def action() -> str:
    return str(datetime.datetime.now())
        """
    result = check_and_execute_action_code(msg)
    print(result)


def is_code_prefix(msg:str) -> bool:
    code_prefix = "请帮助我执行如下代码"
    if len(code_prefix) <= len(msg):
        return False
    min_len = min(len(code_prefix), len(msg))
    return code_prefix[:min_len] == msg[:min_len]

def is_code(msg:str) -> bool:
    code_prefix = "请帮助我执行如下代码"
    if len(code_prefix) <= len(msg):
        return code_prefix == msg[:len(code_prefix)]
    return False
    
def get_process_bar(stage:int) -> str:
    stage = min(stage, 9)
    bar_list = ['_'] * 10
    for i in range(stage):
        bar_list[i] = '='
    bar_str = "程序执行中：[" + "".join(bar_list) + "]"
    return bar_str


def predict(message, history):
    logger.info(f"message: {message}, history: {history}")
    history_openai_format = [{"role": "system", "content": SYS_PROMPT}]
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    prompt = f"""{message}"""
    history_openai_format.append({"role": "user", "content": prompt})
    response = call_chatbot(history_openai_format)
    partial_message = ""
    
    for i, chunk in enumerate(response):
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            # if is_code_prefix(partial_message):
            #     continue
            # elif is_code(partial_message):
            #     yield get_process_bar(i // 5)
            # else:
            #     yield partial_message
            yield partial_message

    exec_result = check_and_execute_action_code(partial_message)
    if exec_result is not None:
        predict_result = predict(exec_result, history + [(prompt, partial_message),])
        for delta in predict_result:
            yield partial_message + "\n\n" + delta

if __name__ == "__main__":
    gr.ChatInterface(predict).launch()
    # test_execute_action_code()
    # print(len(SYS_PROMPT))