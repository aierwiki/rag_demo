import baostock as bs
import pandas as pd
from baostock import query_history_k_data_plus as query_history_k_data_plus_inner
from baostock import query_dividend_data as query_dividend_data_inner
from baostock import query_adjust_factor as query_adjust_factor_inner
from baostock import query_profit_data as query_profit_data_inner
from baostock import query_operation_data as query_operation_data_inner
from baostock import query_growth_data as query_growth_data_inner
from baostock import query_balance_data as query_balance_data_inner
from baostock import query_cash_flow_data as query_cash_flow_data_inner
from baostock import query_dupont_data as query_dupont_data_inner
from baostock import query_performance_express_report as query_performance_express_report_inner
from baostock import query_forecast_report as query_forecast_report_inner
from baostock import query_stock_basic as query_stock_basic_inner
from baostock import query_deposit_rate_data as query_deposit_rate_data_inner
from baostock import query_loan_rate_data as query_loan_rate_data_inner
from baostock import query_required_reserve_ratio_data as query_required_reserve_ratio_data_inner
from baostock import query_money_supply_data_month as query_money_supply_data_month_inner
from baostock import query_money_supply_data_year as query_money_supply_data_year_inner
from baostock import query_shibor_data as query_shibor_data_inner
from baostock import query_stock_industry as query_stock_industry_inner
from baostock import query_sz50_stocks as query_sz50_stocks_inner
from baostock import query_hs300_stocks as query_hs300_stocks_inner
from baostock import query_zz500_stocks as query_zz500_stocks_inner

bs.login()

def query_history_k_data_plus(code:str, fields:str, start_date:str=None, end_date:str=None,
                              frequency:str='d', adjustflag:str='3') -> pd.DataFrame:
    ret = query_history_k_data_plus_inner(code, fields, start_date, end_date, frequency, adjustflag)
    ret = ret.get_data()
    # 将 open	high	low	close	preclose	volume	amount	adjustflag	turn	tradestatus	pctChg	isST 的数据类型转换为 float
    for col in ret.columns:
        if col in ['open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'turn', 'pctChg']:
            ret[col] = ret[col].astype(float)
    return ret


def query_dividend_data(code:str, year:str=None, yearType:str="report") -> pd.DataFrame:
    ret = query_dividend_data_inner(code, year, yearType)
    ret = ret.get_data()
    return ret


def query_adjust_factor(code:str, start_date:str=None, end_date:str=None) -> pd.DataFrame:
    ret = query_adjust_factor_inner(code, start_date, end_date)
    ret = ret.get_data()
    return ret

def query_profit_data(code:str, year:str=None, quarter:str=None) -> pd.DataFrame:
    ret = query_profit_data_inner(code, year, quarter)
    ret = ret.get_data()
    return ret


def query_operation_data(code:str, year:str=None, quarter:str=None) -> pd.DataFrame:
    ret = query_operation_data_inner(code, year, quarter)
    ret = ret.get_data()
    return ret


def query_growth_data(code:str, year:str=None, quarter:str=None) -> pd.DataFrame:
    ret = query_growth_data_inner(code, year, quarter)
    ret = ret.get_data()
    return ret

def query_balance_data(code:str, year:str=None, quarter:str=None) -> pd.DataFrame:
    ret = query_balance_data_inner(code, year, quarter)
    ret = ret.get_data()
    return ret

def query_cash_flow_data(code:str, year:str=None, quarter:str=None) -> pd.DataFrame:
    ret = query_cash_flow_data_inner(code, year, quarter)
    ret = ret.get_data()
    return ret


def query_dupont_data(code:str, year:str=None, quarter:str=None) -> pd.DataFrame:
    ret = query_dupont_data_inner(code, year, quarter)
    ret = ret.get_data()
    return ret

def query_performance_express_report(code:str, start_date:str=None, end_date:str=None) -> pd.DataFrame:
    ret = query_performance_express_report_inner(code, start_date, end_date)
    ret = ret.get_data()
    return ret

def query_forecast_report(code:str, start_date:str=None, end_date:str=None) -> pd.DataFrame:
    ret = query_forecast_report_inner(code, start_date, end_date)
    ret = ret.get_data()
    return ret

def query_stock_basic(code:str="", code_name:str="")-> pd.DataFrame:
    ret = query_stock_basic_inner(code, code_name)
    ret = ret.get_data()
    return ret

def query_deposit_rate_data(start_date:str="", end_date:str="") -> pd.DataFrame:
    ret = query_deposit_rate_data_inner(start_date, end_date)
    ret = ret.get_data()
    return ret

def query_loan_rate_data(start_date:str="", end_date:str="") -> pd.DataFrame:
    ret = query_loan_rate_data_inner(start_date, end_date)
    ret = ret.get_data()
    return ret

def query_required_reserve_ratio_data(start_date="", end_date="", yearType="0")-> pd.DataFrame:
    ret = query_required_reserve_ratio_data_inner(start_date, end_date, yearType)
    ret = ret.get_data()
    return ret

def query_money_supply_data_month(start_date="", end_date="") -> pd.DataFrame:
    ret = query_money_supply_data_month_inner(start_date, end_date)
    ret = ret.get_data()
    return ret

def query_money_supply_data_year(start_date="", end_date="") -> pd.DataFrame:
    ret = query_money_supply_data_year_inner(start_date, end_date)
    ret = ret.get_data()
    return ret

def query_shibor_data(start_date="", end_date=""):
    ret = query_shibor_data_inner(start_date, end_date)
    ret = ret.get_data()
    return ret


def query_stock_industry(code="", date=""):
    ret = query_stock_industry_inner(code, date)
    ret = ret.get_data()
    return ret


def query_sz50_stocks(date=""):
    ret = query_sz50_stocks_inner(date)
    ret = ret.get_data()
    return ret


def query_hs300_stocks(date=""):
    ret = query_hs300_stocks_inner(date)
    ret = ret.get_data()
    return ret


def query_zz500_stocks(date=""):
    ret = query_zz500_stocks_inner(date)
    ret = ret.get_data()
    return ret

def main():
    code = "sh.600000"
    fields = "date,open,high,low,close,volume,amount"
    start_date = "2021-01-01"
    end_date = "2021-01-31"
    frequency = "d"
    adjustflag = "3"
    data = query_history_k_data_plus(code, fields, start_date, end_date, frequency, adjustflag)
    print(data.dtypes)
    print(data.head())


if __name__ == "__main__":
    main()

