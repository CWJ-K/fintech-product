import datetime 
import sys
import time
from typing import List, Tuple

import pandas as pd
import requests 
from loguru import logger
from pydantic import BaseModel
from json import JSONDecodeError
import json

import numpy as np
from src.router import Router


class Period:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def generate_dates_in_a_period(self) -> List[str]:
        return pd.date_range(self.start_date, self.end_date).astype(str).tolist()
    

class DataSectionAfter20110731:
    def __init__(self):
        self.section_name = 'data9'
        self.columns_name = 'fields9'


class DataSectionBy20110731:
    def __init__(self):
        self.section_name = 'data8'
        self.columns_name = 'fields8'


class TWSEWeb:
    def __init__(self, date):
        self.date = self.remove_hypens(date)

    def remove_hypens(self, date):
        return date.replace('-', '')
    
    @property
    def url(self):
        return (
            'https://www.twse.com.tw/exchangeReport/MI_INDEX'
            f'?response=json&date={self.date}&type=ALL'
        )
    
    @property
    def request_header(self):
        return {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Host": "www.twse.com.tw",
            "Referer": "https://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
    
    def request_web_content(self):
        time.sleep(10)
        web_contents = requests.get(
            self.url, headers=self.request_header
        )
        return web_contents
    
    def get_required_information_based_on_date(self) -> Tuple[str, str]:
        if self.date > '20110731':
            data_section = DataSectionAfter20110731()
        elif self.date <= '2011731' and self.date >= '20040211':
            data_section = DataSectionBy20110731()       

        return data_section.section_name, data_section.columns_name
    
def get_TWSE_daily_raw_data(date):
    web_response = TWSEWeb(date).request_web_content()
    web_contents = web_response.json()
    section_name, columns_name = TWSEWeb(date).get_required_information_based_on_date()
    data = pd.DataFrame(web_contents[str(section_name)])
    columns = web_contents[str(columns_name)]
    report = {'data': data, 'columns': columns, 'date': date}
    logger.info(f'1 status_code:{web_response.status_code}')
    return report


class StockSchema(BaseModel):
    StockID: str
    TradeVolume: int
    Transaction: int
    TradeValue: int
    Open: float
    Max: float
    Min: float
    Close: float
    Change: float
    date: str

class Report:
    def __init__(self, daily_raw_data):
        self.data = daily_raw_data['data']
        self.columns = daily_raw_data['columns']
        self.date = daily_raw_data['date']
        
    def translate_Chinese_columns_into_English(self):
        TRANSLATION_TABLE = {
            '證券代號': 'StockID',
            '證券名稱': 'StockName', #
            '成交股數': 'TradeVolume',
            '成交筆數': 'Transaction',
            '成交金額': 'TradeValue',
            '開盤價': 'Open',
            '最高價': 'Max',
            '最低價': 'Min',
            '收盤價': 'Close',
            '漲跌(+/-)': 'Dir',
            '漲跌價差': 'Change',
            '最後揭示買價': 'LastBestBidPrice', #
            '最後揭示買量': 'LastBestBidVolume', #
            '最後揭示賣價': 'LastBestAskPrice', #
            '最後揭示賣量': 'LastBestAskVolume', #
            '本益比': 'PriceEarningRatio', #
        }

        english_columns_name = [TRANSLATION_TABLE[chinese_column] for chinese_column in self.columns]
        self.data.columns = english_columns_name
        return self
    
    def parse_dir_symbol(self):
        self.data['Dir'] = self.data['Dir'].str.extract(r'\>(.*?)\<')
        return self
    
    def add_minus_dir_symbol_to_change(self):
        self.data["Change"] = np.where(self.data['Dir']=='-', '-'+self.data['Change'], self.data['Change'])
        return self
    
    def replace_hypens_to_not_applicable(self):
        column_with_hypens = ['Open', 'Max', 'Min', 'Close']
        for column in column_with_hypens:
            self.data[column] = self.data[column].str.replace('--', '0')
        return self
    
    def remove_comma_in_numbers(self):
        self.data = self.data.replace(',', "", regex=True)
        return self
    
    def remove_unused_information(self):
        unused_information = ['StockName', 'LastBestBidPrice', 'LastBestBidVolume', 'LastBestAskPrice', 'LastBestAskVolume', 'PriceEarningRatio', 'Dir']
        self.data = self.data.drop(unused_information, axis=1)
        return self
    
    def add_date(self):
        self.data['date'] = self.date
        return self

        
def create_daily_report(daily_raw_data):
    report = (
        Report(daily_raw_data)
        .translate_Chinese_columns_into_English()
        .parse_dir_symbol()
        .add_minus_dir_symbol_to_change()
        .replace_hypens_to_not_applicable()
        .remove_comma_in_numbers()
        .remove_unused_information()
        .add_date()
        .data
        .fillna("")
    )
    return report


def check_report(data: pd.DataFrame) -> pd.DataFrame:
    data_dict = data.to_dict('records')
    df_schema = [
        StockSchema(**elements).__dict__
        for elements in data_dict
    ]
    results = pd.DataFrame(df_schema)
    return results


def save_daily_report(date, report):
    db_router = Router()
    try:
        report.to_sql(
            name='TaiwanStockPrice',
            con=db_router.mysql_financialdata_conn,
            if_exists='append',
            index=False,
            chunksize=1000
        )
    except Exception as e:
        logger.info(e)
    
    
def check_date(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    weekday = date.weekday() + 1
    no_data_date = datetime.datetime.strptime('2004-02-11', '%Y-%m-%d')
    if date < no_data_date or weekday == 6 or weekday == 7:
        return False
    else:
        return True
    
    
def produce_daily_report(date):
    flag = True
    while flag:
        try:
            daily_raw_data = get_TWSE_daily_raw_data(date)
            daily_report = create_daily_report(daily_raw_data)
            report = check_report(daily_report)
            save_daily_report(date, report)
            flag = False
            return report
            
        except JSONDecodeError:
            logger.info('JSONDecodeError: Internet issue, retry until success')
            time.sleep(30)

        except KeyError:
            logger.info(f'date:{date} => no data if date is before 2004-02-11 or date is Sunday or Saturdy')
            flag = False
            return pd.DataFrame()

        
def main(start_date, end_date):
    dates = Period(start_date, end_date).generate_dates_in_a_period()
    for date in dates:
        logger.info(f'start to product {date} report')
        produce_daily_report(date)

        
if __name__ == '__main__':
    start_date, end_date = sys.argv[1:]
    main(start_date, end_date)