import requests
import time
import requests
import time
import os
import hashlib
import uuid
from loguru import logger
from typing import List, Tuple, Dict, Union, Set
from openai import OpenAI



class ChatBot:
    def __init__(self):
        self.url = 'https://api.deepseek.com'
        app_key = os.environ.get('DEEPSEEK_API_KEY', None)
        if app_key is None:
            raise Exception('DEEPSEEK_API_KEY not found in env')
        self.app_key = app_key
        self.client = OpenAI(api_key=self.app_key, base_url="https://api.deepseek.com")
    
    def ask(self, query:str, history:List[Tuple[str]]=[], system_prompt:str=None, log=False):
        # 先检查一下缓存中是否存在
        path = os.path.dirname(os.path.abspath(__file__))
        cache_dir = os.path.join(path, 'cache')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        sha1val = hashlib.sha1(query.encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f'{sha1val}.txt')
        if os.path.exists(cache_file):
            logger.info(f"cache hit: {cache_file}")
            with open(cache_file, 'r', encoding='utf-8') as f:
                response = f.read()
            return response
        logger.info(f"query len : {len(query)}")
        message_list = []
        for q, a in history:
            message_list.append({"role": "user", "content": q})
            message_list.append({"role": "assistant", "content": a})
        message_list.append({"role": "user", "content": query})
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=message_list,
                max_tokens=4096,
                temperature=0.9
            )
            response = response.choices[0].message.content
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(response)
        except Exception as e:
            logger.error(e)
            response = ""
        logger.info(f"response len : {len(response)}")
        
        return response
    

if __name__ == '__main__':
    chat_bot = ChatBot()
    response = chat_bot.ask('你好', log=True)
    print(response)