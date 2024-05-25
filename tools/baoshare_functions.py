import baostock as bs
import pandas as pd
from baostock import query_history_k_data_plus as query_history_k_data_plus_inner

bs.login()

def query_history_k_data_plus(code, fields, start_date=None, end_date=None,
                              frequency='d', adjustflag='3') -> pd.DataFrame:
    ret = query_history_k_data_plus_inner(code, fields, start_date, end_date, frequency, adjustflag)
    ret = ret.get_data()
    return ret




