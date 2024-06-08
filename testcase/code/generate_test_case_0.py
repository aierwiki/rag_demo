import random
import string
import json
import pandas as pd

def generate_test_cases(num_cases=2):
    test_cases = []
    for _ in range(num_cases):
        # 随机生成股票代码
        code = str(random.randint(605000,605999))
        stock_code = f"sh.{code}" if random.choice([True, False]) else f"sz.{code}"
        
        # 随机选择字段
        fields = ','.join(random.choices(['date', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'adjustflag', 'turn', 'tradestatus', 'pctChg', 'peTTM', 'pbMRQ', 'psTTM', 'pcfNcfTTM', 'isST'], k=random.randint(1, 5)))

        # 随机生成开始和结束日期
        start_date_year = random.randint(2010, 2024)
        start_date_month = random.randint(1, 12)
        start_date_day = random.randint(1, 28)
        end_date_year = random.randint(start_date_year, 2024)
        end_date_month = random.randint(start_date_month, 12) if end_date_year == start_date_year else random.randint(1, 12)
        end_date_day = random.randint(start_date_day, 28) if end_date_month == start_date_month else random.randint(1, 28)
        start_date = "{:4}-{:02}-{:02}".format(start_date_year, start_date_month, start_date_day)
        end_date = "{:4}-{:02}-{:02}".format(end_date_year, end_date_month, end_date_day)

        # 随机选择频率
        frequency = random.choice(['d', 'w', 'm', '5', '15', '30', '60'])
        
        # 随机选择复权类型
        adjustflag = random.choice(['1', '2', '3'])
        
        # 构造输入参数
        input_params = {
            "code": stock_code,
            "fields": fields,
            "start_date": start_date,
            "end_date": end_date,
            "frequency": frequency,
            "adjustflag": adjustflag
        }
        
        # 随机选择期望返回的列名
        expected_columns = random.sample(input_params["fields"].split(','), random.randint(1, len(input_params["fields"].split(','))))
        
        # 添加到测试用例列表
        test_cases.append({
            "input_params": input_params,
            "expected_columns": expected_columns
        })
    
    return test_cases

# 生成测试用例
test_cases = generate_test_cases(5)
for case in test_cases:
    print(json.dumps(case, indent=4))