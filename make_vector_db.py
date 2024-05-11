import os
import json
from typing import List, Tuple, Dict
import joblib
import numpy as np
from zhipuai import ZhipuAI

API_KEY = os.getenv("ZHIPU_API_KEY", None)
if API_KEY is None:
    raise ValueError("Please set the ZHIPU_API_KEY environment variable.")

embedding_client = ZhipuAI(api_key=API_KEY)


def split_origin_text_using_strategy(txt_content:str) -> List[str]:
    # 真实场景中的文本切分策略会比较复杂，这里用一个简单的策略来演示
    # 使用连续空行来切分文本
    snippets = txt_content.split("\n\n")
    return snippets


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(path, "data")
    txt_file = os.path.join(data_path, "common_qa.txt")
    with open(txt_file, "r") as f:
        txt_content = f.read()
    # 1. 使用策略对原始的长文本进行切分
    snippets = split_origin_text_using_strategy(txt_content)

    # 2. 将切分得到的文本片段进行向量化
    vectors = []
    for snippet in snippets:
        response = embedding_client.embeddings.create(
            model="embedding-2", #填写需要调用的模型名称
            input=snippet,
        )
        vec = np.array(response.data[0].embedding)
        vectors.append(vec)

    # 3. 将向量化的结果保存到数据库中
    vectors = np.array(vectors)
    
    joblib.dump(vectors, os.path.join(data_path, "vector_db.pkl"))
    joblib.dump(snippets, os.path.join(data_path, "snippets.pkl"))
    with open(os.path.join(data_path, "snippets.json"), "w") as f:
        json.dump(snippets, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()


