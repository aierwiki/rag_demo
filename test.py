import os
import json
import re


def _get_info():
    return "本地信息如下：xxx"


def main():
    code_str = """
def get_info():
    info =  _get_info()
    return info
"""
    global_vars = {"_get_info": _get_info}
    exec(code_str, global_vars)
    info = global_vars['get_info']()
    print(info)
    


def parse_json() -> dict:
    json_str = """
        ```json
        {
            "key": "value",
            "key2": "value2"
        }
        ```
    """
    pattern = r'\{.*\}'
    match = re.match(pattern, json_str, re.DOTALL)

    if match:
        # 提取匹配的 JSON 部分
        json_string = match.group(0)
        
        # 将 JSON 字符串转换为词典
        dictionary = json.loads(json_string)
        
        # 打印词典
        print(dictionary)
    else:
        print("No JSON found")

    
if __name__ == '__main__':
    main()
    # parse_json()